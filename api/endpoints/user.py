from typing import List

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_schema import UserSchema

from core.database import get_session
from repositories.user import UserRepository


router = APIRouter()

user_repository = UserRepository()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def creater_user(user: UserSchema, db: AsyncSession = Depends(get_session)):
    result = await user_repository.create(user=user, db=db)
    return result


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_session)):
    result = await user_repository.list_users(db=db)
    return result


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await user_repository.show(id=user_id, db=db)
    return result


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserSchema)
async def put_user(user_id: int, user: UserSchema, db: AsyncSession = Depends(get_session)):
    result = await user_repository.alter(id=user_id, body=user, db=db)
    return result


@router.delete('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await user_repository.delete(id=user_id, db=db)
    return result
        

