from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from ai.extractor import extract_params
from ai.query_builder import build_query
from schemas.apartment import ApartmentListOut
from schemas.search import SearchRequest

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=ApartmentListOut)
async def ai_search(
    body: SearchRequest,
    session: AsyncSession = Depends(get_session),
) -> ApartmentListOut:
    params = extract_params(body.query)
    stmt = build_query(params)
    result = await session.execute(stmt)
    items = result.scalars().all()
    return ApartmentListOut(total=len(items), items=items)