import datetime

from sqlmodel import Field, SQLModel

from sqlalchemy.types import DateTime

from typing import Optional


class BookModel(SQLModel, table=True):
    __tablename__: str = 'book'

    id: Optional[int] = Field(default=True, primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    author: str = Field(max_length=100, nullable=False)
    created_at: Optional[DateTime] = Field(default=datetime.datetime.now, nullable=False)