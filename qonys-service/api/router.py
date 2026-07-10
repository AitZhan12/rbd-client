from fastapi import APIRouter

from api.v1.endpoints import ai_search
from api.v1.router import api_v1_router
from core.config import settings

api_router = APIRouter()
api_router.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)