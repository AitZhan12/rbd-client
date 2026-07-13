import asyncio
import logging

from ai.llm import process_item_llm
from db.crud import get_batch, save_llm_memo
from db.db import async_session

BATCH_SIZE = 1000

def is_kazakh(text: str) -> bool:
    kazakh_chars = set("әғқңөұүһі")
    return any(c in kazakh_chars for c in text.lower())


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