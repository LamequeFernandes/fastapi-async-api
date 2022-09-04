# from os import stat_result
# from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# from pydantic import BaseModel

# from core.database import Session
from core.auth import oauth2_schema
from core.config import settings
from models.user_model import UserModel
from core.database import get_session


# class TokenData(BaseModel):

async def get_current_user(
    db: AsyncSession=Depends(get_session), 
    token: str=Depends(oauth2_schema)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possivel autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            key=settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')

        if username is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(username))
        result = await session.execute(query)
        user: UserModel = result.scalar()

        if user is None:
            raise credential_exception
        
        return user