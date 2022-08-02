import datetime

from sqlmodel import Field, SQLModel

from typing import Optional


class BookModel(SQLModel, table=True):
    __tablename__: str = 'book'

    id: Optional[int] = Field(default=True, primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    author: str = Field(max_length=100, nullable=False)
    created_at: Optional[str] = Field(default=datetime.datetime.now, nullable=False)