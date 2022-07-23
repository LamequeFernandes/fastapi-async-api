from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    id: Optional[int]
    title: str
    created_at: str

    class Config:
        orm_mode = True