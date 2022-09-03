from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

from core.config import settings

from datetime import datetime


class RendaModel(settings.Base):
    __tablename__ = 'renda_mensal'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    amount: float = Column(Float, nullable=False)
    description: str = Column(String(256), nullable=False)
    user: int = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    update_at: DateTime = Column(DateTime)
    created_at: DateTime = Column(DateTime, default=datetime.now(), nullable=False)
