from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchema

from core.database import get_session


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def creater_user(user: UserSchema, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(**user.dict())
    # new_user = UserModel(name=user.name, email=user.email, password=user.password)

    db.add(new_user)
    await db.commit()
    print(new_user.id)

    return new_user


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().all()

        if users:
            print(users)
            return users
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum usuário encontrado')


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()

        if user:
            return user
        raise HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserSchema)
async def put_user(user_id: int, user: UserSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_up: UserModel = result.scalar_one_or_none()

        if user_up:
            user_up.email = user.email
            user_up.name = user.name
            user_up.password = user.password
            
            await session.commit()

            return user_up
        return HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)


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
        return HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

