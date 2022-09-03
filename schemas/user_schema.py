from typing import Optional, Any

from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    id: Optional[int]
    name: str
    email: str
    is_admin: Optional[bool]
    created_at: Optional[Any]

    class Config:
        orm_mode = True

class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaUp(UserSchemaBase):
    name: Optional[str]
    email: Optional[str]
    is_admin: Optional[bool]
    password: Optional[str]