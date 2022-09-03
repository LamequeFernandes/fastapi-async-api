from typing import List

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUp

from core.database import get_session
# from core.deps import get_current_user
from repositories.user_repository import UserRepository


router = APIRouter()

user_repository = UserRepository()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchemaCreate)
async def creater_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    result = await user_repository.create(user=user, db=db)
    return result


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    result = await user_repository.list_users(db=db)
    return result


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserSchemaBase)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await user_repository.show(id=user_id, db=db)
    return result


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserSchemaUp)
async def put_user(user_id: int, user: UserSchemaUp, db: AsyncSession = Depends(get_session)):
    result = await user_repository.alter(id=user_id, body=user, db=db)
    return result


@router.delete('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await user_repository.delete(id=user_id, db=db)
    return result
        

