import asyncio
import json
import logging
import os

import requests
from requests import Session

from db.crud import update_apartments
from scraper.filters import build_payload_get
from scraper.main import get_login, make_request, extract_photo_urls

from config import settings


async def get_details(source_ids):
    session: Session = requests.Session()
    get_login(session)

    items = []

    for source_id in source_ids:
        obj = {'source_id': source_id, 'photo': None, 'phone': None}

        # payload = build_payload_get(source_id)
        payload = build_payload_get(source_id)
        details = make_request(session, settings.GET_URL, payload=payload, method="POST")
        if not details:
            logging.warning(f"Failed to fetch details for apartment ID: {source_id}")
        photos = details.get('photo', [])
        if photos:
            photo = extract_photo_urls(photos)
            obj['photo'] = photo
        else:
            logging.warning(f"No photos found for apartment ID: {source_id}")

        phone = details.get('phone', [])
        if phone:
            phone = [x.get('phoneNumber', '') for x in phone]
            obj['phone'] = phone
        else:
            logging.warning(f"No phone number found for apartment ID: {source_id}")

        items.append(obj)
    await update_apartments(items)

async def main():
    if not os.path.exists(settings.FILES_DIR / 'list_ids.json'):
        logging.error("list_ids.json not found")
        return

    with open(settings.FILES_DIR / 'list_ids.json') as f:
        list_ids = json.load(f)
        await get_details(list_ids)


if __name__ == "__main__":
    asyncio.run(main())