from sqlalchemy import Column, Integer, String, DateTime

from core.config import settings

import datetime


class UserModel(settings.Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(100), nullable=False)
    email: str = Column(String(200), nullable=False)
    password: str = Column(String(80), nullable=False)
    created_at: DateTime = Column(DateTime, default=datetime.datetime.now, nullable=False)
