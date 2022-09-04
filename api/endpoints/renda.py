from typing import List

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import UserModel

from schemas.renda_schema import RendaSchema, RendaSchemaUp

from core.database import get_session
from core.deps import get_current_user
from repositories.renda_repository import RendaRepository


router = APIRouter()

renda_repository = RendaRepository()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RendaSchema)
async def post_renda(
    renda: RendaSchema, 
    user_logged: UserModel = Depends(get_current_user), 
    db: AsyncSession = Depends(get_session)
):
    return await renda_repository.insert(renda, user_logged.id, db)


@router.get('/{id}', response_model=RendaSchema)
async def get_renda(id: int, db: AsyncSession = Depends(get_session)):
    return await renda_repository.show(id, db)


@router.get('/', response_model=RendaSchema)
async def get_all_renda(db: AsyncSession = Depends(get_session)):
    return await renda_repository.list_all(db)


@router.delete('/{id}', response_model=RendaSchema)
async def delete_renda(id: int, db: AsyncSession = Depends(get_session)):
    return await renda_repository.delete(id, db)

