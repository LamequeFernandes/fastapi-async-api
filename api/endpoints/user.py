from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchema

from database.database import get_session


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def creater_user(user: UserSchema, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(**user.dict())
    # new_user = UserModel(name=user.name, email=user.email, password=user.password)

    db.add(new_user)
    await db.commit()
    print(new_user.id)

    return new_user


@router.get('/', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().all()

        if users:
            return users
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum usuário encontrado')


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()

        if user:
            return user
        return HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)
