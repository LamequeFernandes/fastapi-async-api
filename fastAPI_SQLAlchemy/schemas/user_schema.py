from typing import Optional, Any

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    created_at: Optional[Any]

    class Config:
        orm_mode = True