from typing import Optional

from sqlmodel import Field, SQLModel

import datetime


class UserModel(SQLModel, table=True):
    __tablename__: str = 'user'

    id: Optional[int] = Field(default=True, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=200, nullable=False)
    password: str = Field(max_length=80)
    created_at: Optional[str] = Field(default=datetime.datetime.now)