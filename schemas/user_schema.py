from typing import Optional, Any

from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    is_admin: Optional[bool]
    created_at: Optional[Any]

    class Config:
        orm_mode = True

class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaUp(UserSchemaBase):
    name: Optional[str]
    email: Optional[EmailStr]
    is_admin: Optional[bool]
    password: Optional[str]