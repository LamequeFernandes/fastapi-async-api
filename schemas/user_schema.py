from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    created_at: str

    class Config:
        orm_mode = True