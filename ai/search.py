import asyncio
import logging

from ai.extractor import extract_params
from ai.query_builder import build_query
from db.db import async_session


async def search(user_query: str):
    params = extract_params(user_query)
    logging.info(f"Извлечено: {params}")

    print(build_query(params))
    async with async_session() as session:
        result = await session.execute(build_query(params))
        apartments = result.scalars().all()

    return apartments


# использование
async def main():
    query = "Ищу квартиру в районе дендрапарка, 2 комнаты, нижние этажи, хороший ремонт"
    results = await search(query)
    for apt in results:
        print(f"{apt.room_count}-комн, {apt.area}м², {apt.floor_num}/{apt.floor_count} эт, "
              f"{apt.price:,.0f}₸ — {apt.district_text} — общ.{apt.memo_public}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())