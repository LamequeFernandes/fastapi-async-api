from sqlmodel import SQLModel

from db.database import engine


async def create_table() -> None:
    import models.__all_models
    print('Criando as tabelas no banco de dados...')

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)
    print('Tabelas criadas')



if __name__ == '__main__':
    import asyncio

    asyncio.run(create_table())