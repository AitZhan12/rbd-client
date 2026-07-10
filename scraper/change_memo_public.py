import asyncio
import logging
import time

import requests

from db.crud import get_batch, save_llm_memo
from db.db import async_session

BATCH_SIZE = 1000
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "second_constantine/t-lite-it-2.1:8b"


def query_llm(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            r = requests.post(OLLAMA_URL, json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
            }, timeout=300)
            return r.json()["response"]
        except (requests.ConnectionError, requests.Timeout) as e:
            logging.warning(f"LLM retry {attempt+1}/{retries}: {e}")
            time.sleep(5)
    return ""


def is_kazakh(text: str) -> bool:
    kazakh_chars = set("әғқңөұүһі")
    return any(c in kazakh_chars for c in text.lower())


async def process_item_llm(item):
    prompt = f"""Перепиши объявление другими словами, сохранив весь смысл.
                 Меняй формулировки и порядок предложений, но НЕ добавляй новых фактов и характеристик.
                 Верни ТОЛЬКО переписанный текст.
                 Текст: {item}"""
    response = query_llm(prompt)
    return response


async def main():
    while True:
        async with async_session() as session:
            batch = await get_batch(session, limit=BATCH_SIZE)
            if not batch:
                logging.info("Все записи обработаны")
                break
            for i, item in enumerate(batch, 1):
                if not item.memo_public:
                    continue

                if is_kazakh(item.memo_public):
                    logging.info(f"ID {item.source_id}: пропущен (казахский)")
                    continue

                r = await process_item_llm(item.memo_public)
                if not r:
                    continue

                logging.info(f"ID {item.source_id}: {r[:30]}")
                await save_llm_memo(session, item, r)
                if i % 50 == 0:
                    await session.commit()
                    logging.info(f"50 saved")
            await session.commit()
            logging.info(f"all saved")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    asyncio.run(main())