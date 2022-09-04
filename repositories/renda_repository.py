from typing import List
from unittest import result

from models.renda_model import RendaModel

from fastapi import HTTPException, status

from schemas.renda_schema import RendaSchema, RendaSchemaUp

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class RendaRepository:
    
    async def insert(self, renda: RendaSchema, id_user: int, db: AsyncSession):
        new_renda: RendaModel = RendaModel(
            amount=renda.amount,
            description=renda.description,
            user=id_user
        )

        db.add(new_renda)
        await db.commit()

        return new_renda

    async def show(self, id: int, db: AsyncSession):
        async with db as session:
            query = select(RendaModel).filter(RendaModel.id == id)
            result = await session.execute(query)
            renda = result.scalar()

            if renda:
                return renda
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Renda não encontrada.")
    
    async def list_all(self, db: AsyncSession):
        async with db as session:
            query = select(RendaModel)
            result = await session.execute(query)
            rendas = result.scalars().all()

            if rendas:
                return rendas
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhuma renda encontrada.")
    
    async def delete(self, id: int, db: AsyncSession):
        async with db as session:
            query = select(RendaModel).filter(RendaModel.id == id)
            result = await session.execute(query)
            renda = result.scalar()

            if renda:
                await db.delete(renda)
                await db.commit()
                return dict(mensage="Usuario deletado com sucesso!")
                
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Renda não encontrada.")