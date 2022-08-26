from unittest import result
from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user_model import UserModel
from core.config import settings
from core.security import checked_password

from pydantic import EmailStr


oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'/usuarios/login'
)


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None
        
        if not checked_password(password, user.password):
            return None

        return user


