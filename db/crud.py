import json
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from scraper.dataclass import map_item_to_row
from db.db import async_session
from models.apartment import Apartment


async def upsert_apartments(items: list[dict]):
    rows = [map_item_to_row(it) for it in items]

    unique = {}
    duplicates = []

    for row in rows:
        key = (row["source"], row["source_id"])
        if key in unique:
            duplicates.append(row)
        unique[key] = row
    rows = list(unique.values())

    if duplicates:
        with open("duplicates.json", "a", encoding="utf-8") as f:
            for d in duplicates:
                f.write(json.dumps(d, ensure_ascii=False, default=str) + "\n")

    async with async_session() as session:
        stmt = insert(Apartment).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["source", "source_id"],
            set_={
                "price": stmt.excluded.price,
                "price_meter": stmt.excluded.price_meter,
                "dt_modify": stmt.excluded.dt_modify,
                "updated_at": datetime.now(),
                "photo": stmt.excluded.photo,
                "phone": stmt.excluded.phone,
                "deal_type": stmt.excluded.deal_type,
            },
        )
        await session.execute(stmt)
        await session.commit()


async def update_apartments(items: list[dict]):
    async with async_session() as session:
        for item in items:
            stmt = (
                Apartment.__table__.update()
                .where(Apartment.source_id == item['source_id'])
                .values(
                    photo=item.get('photo'),
                    phone=item.get('phone'),
                    updated_at=datetime.now()
                )
            )
            await session.execute(stmt)
        await session.commit()


async def get_missing_photo_ids() -> list[int]:
    async with async_session() as session:
        result = await session.execute(
            select(Apartment.source_id).where(
                Apartment.photo == None,
                Apartment.phone == None
            )
        )
        return result.scalars().all()


async def get_source_ids_by_price(price) -> list[int]:
    async with async_session() as session:
        result = await session.execute(
            select(Apartment.source_id).where(
                Apartment.price == price,
            )
        )
        return result.scalars().all()


async def change_deal(source_id, param):
    async with async_session() as session:
        await session.execute(
            update(Apartment)
            .where(Apartment.source_id == source_id)
            .values(deal_type=param)
        )
        await session.commit()


async def get_batch(session, limit: int = 1000):
    result = await session.execute(
        select(Apartment)
        .order_by(Apartment.dt_create.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def save_llm_memo(session, item, rewritten: str):
    await session.execute(
        update(Apartment)
        .where(Apartment.source_id == item.source_id)
        .values(memo_rewritten=rewritten)
    )