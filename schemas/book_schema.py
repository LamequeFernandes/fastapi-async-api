from typing import Any, Optional

from pydantic import BaseModel


class BookSchema(BaseModel):
    id: Optional[int]
    title: str
    created_at: Optional[Any]

    class Config:
        orm_mode = True