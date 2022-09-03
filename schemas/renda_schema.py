from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class RendaSchema(BaseModel):
    id: Optional[int]
    amount: float
    description: str
    user: int
    update_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class RendaSchemaUp(RendaSchema):
    amount: Optional[float]
    description: Optional[str]
    user: Optional[int]
    update_at: Optional[datetime]
    created_at: Optional[datetime]