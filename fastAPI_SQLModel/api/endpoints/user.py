from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import UserModel

from sqlmodel import select

from db.database import get_session

from typing import List


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def post_user(user: UserModel, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(**user.dict())

    db.add(new_user)
    await db.commit()

    return new_user


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserModel])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().all()

        return users


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()
        if user:
            return user
        raise HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserModel)
async def put_user(user_id: int, user: UserModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_up: UserModel = result.scalar_one_or_none()

        if user_up:
            user_up = UserModel(**user)

            await session.commit()
        raise HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()

        if user:
            await session.delete(user)
            await session.commit()

            return {"messagem": "Usuario deletado com sucesso"}
        raise HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)
