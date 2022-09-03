from fastapi import APIRouter

from api.endpoints import user
from api.endpoints import renda


api_router = APIRouter()
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(renda.router, prefix='/renda', tags=['renda'])