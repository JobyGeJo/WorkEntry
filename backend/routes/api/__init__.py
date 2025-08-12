from fastapi import APIRouter

from .v1 import v1

api_router = APIRouter(prefix="/api")
api_router.include_router(v1)