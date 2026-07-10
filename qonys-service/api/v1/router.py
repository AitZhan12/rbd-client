from fastapi import APIRouter

from api.v1.endpoints import ai_search, health

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(ai_search.router)
