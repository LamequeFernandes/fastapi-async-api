from typing import List

from models.user_model import UserModel

from fastapi import HTTPException, status

from schemas.user_schema import UserSchemaCreate, UserSchemaUp
from core.security import checked_password, generate_hash_password

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class UserRepository:

    async def user_exists(self, id: int, db: AsyncSession):
        async with db as session:
            query_user = select(UserModel).filter(UserModel.id == id)
            result_query = await session.execute(query_user)
            user: UserModel = result_query.scalar()

            if not user:
                return None
            return user

    async def create(self, user: UserSchemaCreate, db: AsyncSession):
        try:
            new_user: UserModel = UserModel(
                name=user.name,
                email=user.email,
                password=generate_hash_password(user.password),
                is_admin=user.is_admin
            )
            db.add(new_user)
            await db.commit()
        except Exception as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Exeção -> {erro}")

        return new_user
    
    async def list_users(self, db: AsyncSession):
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
    
    async def show(self, id: int, db: AsyncSession):
        user = await self.user_exists(id=id, db=db)

        if not user:
            raise HTTPException(detail='Usuario não encontrado', 
                                status_code=status.HTTP_404_NOT_FOUND)            
        return user

    async def delete(self, id: int, db: AsyncSession):
        user = await self.user_exists(id=id, db=db)

        if not user:
            raise HTTPException(detail='Usuario não encontrado', 
                                status_code=status.HTTP_404_NOT_FOUND) 

        async with db as session:
            await session.delete(user)
            await session.commit()

            return dict(message = "Usuario deletado com sucesso")

    async def alter(self, id: int, body: UserSchemaUp, db: AsyncSession):
            
        async with db as session:
            query_user = select(UserModel).filter(UserModel.id == id)
            result_query = await session.execute(query_user)
            user: UserModel = result_query.scalar()

            if not user:
                raise HTTPException(detail='Usuario não encontrado', 
                                    status_code=status.HTTP_404_NOT_FOUND)

            body = body.dict()
            for key in body:
                if body[key] != None:
                    setattr(user, key, body[key])

            await session.commit()
            return user
