from core.config import settings
from core.database import engine


async def create_tables() -> None:
    import models.__all_models     # deve-se importar todas models que se deseja criar no DB
    print('Criando tabelas')

    async with engine.begin() as connection:
        await connection.run_sync(settings.Base.metadata.drop_all)
        await connection.run_sync(settings.Base.metadata.create_all)
    print('Tabelas criadas')


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())