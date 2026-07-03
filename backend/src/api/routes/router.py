from fastapi import APIRouter
from src.api.routes.endpoints import health, rag

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(rag.router, prefix="/rag")