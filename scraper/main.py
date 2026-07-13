import argparse
import asyncio
import os
import random
import logging
from datetime import date

import requests, json, time
from requests import Session

from scraper.change_memo_public import is_kazakh, process_item_llm
from scraper.checkpoint import load_checkpoint, save_checkpoint, clear_checkpoint
from scraper.dataclass import SearchFilters
from db.crud import upsert_apartments

from scraper.filters import build_payload, build_payload_get
from config import settings


log_file = os.getenv("LOG_FILE", "../scraper.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

headers = {
    "Mb-Ajax": "true",
    "Origin": "https://rbd.kz",
    "Referer": "https://rbd.kz/app/demand/start"
}

def get_login(session: Session):
    username = settings.RBD_EMAIL
    password = settings.RBD_PASSWORD
    url = settings.LOGIN_URL

    payload = {
            "type":"databox","value":{
            "email":{"type":"string","value":username},
            "passwd":{"type":"string","value":password},
            "remember":{"type":"boolean","value":True}
        }}

    headers = {
        "Mb-Ajax": "true",
        "Origin": "https://rbd.kz",
        "Referer": "https://rbd.kz/site/login",
    }
    files = {"data": (None, json.dumps(payload))}
    r = session.post(url, headers=headers, files=files)
    if r.status_code == 200:
        logging.info("Login successful")
    else:
        logging.error(f"Login failed with status code {r.status_code}")
        raise Exception("Login failed")


def make_request(session: Session, url: str, payload: dict = None, method: str = "POST",
                 _retries: int = 3) -> dict | None:
    files = {"data": (None, json.dumps(payload))} if payload else None

    for attempt in range(_retries):
        r = session.request(method, url, headers=headers, files=files)

        if r.status_code == 200:
            return r.json()

        if r.status_code == 401:
            logging.warning("401 - re-login")
            get_login(session)
            continue

        logging.warning(f"Attempt {attempt + 1}/{_retries} failed with status {r.status_code}")
        logging.warning(f"Error: {r.text}")
        time.sleep(1)

    logging.error(f"All {_retries} attempts failed for URL: {url}")
    return None


def extract_photo_urls(photos: list) -> list[dict]:
    url_keys = {"urlBig", "urlSmall", "urlTiny", "urlOriginal"}
    return [
        {k: v for k, v in photo.items() if k in url_keys}
        for photo in photos
    ]


async def enrich_item(session, data):
    batch = []
    for item in data:
        details_payload = build_payload_get(item['id'])
        details = make_request(session, settings.GET_URL, payload=details_payload, method="POST")
        if not details:
            logging.warning(f"Failed to fetch details for apartment ID: {item['id']}")
            continue

        photos= details.get('photo', [])
        if photos:
            item['photo'] = extract_photo_urls(photos)
        else:
            logging.warning(f"No photos found for apartment ID: {item['id']}")

        phone = details.get('phone', [])
        if phone:
            item['phone'] = [x.get('phoneNumber', '') for x in phone]
        else:
            logging.warning(f"No phone number found for apartment ID: {item['id']}")

        supply = details.get('supply', {})
        memo = supply.get('memoPublic', '')
        if not is_kazakh(memo):
            r = await process_item_llm(memo)
            if r:
                item['memo_rewritten'] = r
            
        batch.append(item)
        logging.info(f'Successfully enriched apartment ID: {item["id"]}')
        await asyncio.sleep(random.uniform(0.1, 0.5))
    return batch


async def get_list_apartments(filters: SearchFilters):
    today = date.today().isoformat()
    session: Session = requests.Session()

    get_login(session)

    payload = build_payload(filters, page=1)
    data = make_request(session, settings.LIST_URL, payload=payload, method="POST")

    total = data['count']
    store = data['store']
    per_page = len(store) or 15
    total_pages = (total + per_page - 1) // per_page
    logging.info(f"Всего: {total}, страниц: {total_pages}")

    batch = await enrich_item(session, store)

    start_page, saved_total = load_checkpoint()
    for page in range(start_page, total_pages + 1):
        payload = build_payload(filters, page=page)
        data = make_request(session, settings.LIST_URL, payload=payload, method="POST")
        store = data["store"]

        if not store:
            break

        if filters.new:
            store = [
                item for item in store
                if item.get("dtCreate", "")[:10] == today
            ]
            if not store:
                logging.info("No more today's listings, stopping")
                break


        batch.extend(await enrich_item(session, store))
        logging.info(f"Стр. {page}/{total_pages}, собрано: {len(batch)}")

        if page % 10 == 0:
            await upsert_apartments(batch)
            saved_total += len(batch)
            logging.info(f"→ записано в БД: {saved_total}")
            batch = []
            save_checkpoint(page + 1, saved_total)

        print( f"Стр. {page}/{total_pages}, собрано: {len(batch)}")
        await asyncio.sleep(random.uniform(0.5, 1.2))

    if batch:
        await upsert_apartments(batch)
        saved_total += len(batch)

    clear_checkpoint()
    logging.info(f"Готово. Сохранено: {saved_total}")
    print(f"Готово. Сохранено: {saved_total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RBD scraper")
    parser.add_argument("--city", type=int, default=4)
    parser.add_argument("--sell", action="store_true")
    parser.add_argument("--lease", action="store_true")
    parser.add_argument("--rooms", type=str, default=None)
    parser.add_argument("--source", type=int, default=2)
    parser.add_argument("--new", action="store_true", default=True)
    args = parser.parse_args()
    print(f'--sell: {args.sell}')
    print(f'--lease: {args.lease}')
    print(f'--new: {args.new}')
    filters = SearchFilters(city=4, sell=args.sell, lease=args.lease, rooms=args.rooms, source=args.source, new=args.new)
    asyncio.run(get_list_apartments(filters))