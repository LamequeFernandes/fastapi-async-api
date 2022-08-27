from typing import List
from unittest import result

from models.user_model import UserModel

from fastapi import HTTPException, status

from schemas.user_schema import UserSchema

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select


class UserRepository:

    @staticmethod
    async def create(user: UserSchema, db: AsyncSession):
        try:
            new_user: UserSchema = UserModel(**user.dict())

            db.add(new_user)
            await db.commit()
        except Exception as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Exeção -> {erro}")

        return new_user
    
    @staticmethod
    async def list_users(db: AsyncSession):
        async with db as session:
            try:
                query = select(UserModel)
                result = await session.execute(query)
                users = result.scalars().all()
            except Exception as erro:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail=erro)
            if not users:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Nenhum usuário encontrado')
            return users
    

