from typing import List

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
                query_users = select(UserModel).order_by(UserModel.id)
                result = await session.execute(query_users)
                users: List[UserModel] = result.scalars().all()
            except Exception as erro:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail=erro)
            if not users:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Nenhum usuário encontrado')
            return users
    
    @staticmethod
    async def show(id: int, db: AsyncSession):
        async with db as session:
            try:
                query_user = select(UserModel).filter(UserModel.id == id)
                result_query = await session.execute(query_user)
                user: UserModel = result_query.scalar()
            except Exception as error:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail=error)
            if not user:
                raise HTTPException(detail='Usuario não encontrado', 
                                    status_code=status.HTTP_404_NOT_FOUND)

            return user

    @staticmethod
    async def delete(id: int, db: AsyncSession):
        async with db as session:
            query_user = select(UserModel).filter(UserModel.id == id)
            result_query = await session.execute(query_user)
            user_delete = result_query.scalar()

            if not user_delete: 
                raise HTTPException(detail='Usuario não encontrado', 
                                    status_code=status.HTTP_404_NOT_FOUND)
            
            await session.delete(user_delete)
            await session.commit()

            return dict(message = "Usuario deletado com sucesso")

    @staticmethod
    async def alter(id: int, body: UserSchema, db: AsyncSession):
        async with db as session:
            query_user = select(UserModel).filter(UserModel.id == id)
            result_query = await session.execute(query_user)
            user: UserModel = result_query.scalar()

            if user:
                body = body.dict()

                for key in body:
                    if body[key] != None:
                        setattr(user, key, body[key])

                await session.commit()
                return user

            raise HTTPException(detail='Usuario não encontrado', 
                                status_code=status.HTTP_404_NOT_FOUND)
