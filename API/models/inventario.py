from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class InventarioBase(BaseModel):
    autoparte_id: int
    stock_actual: int = 0
    stock_minimo: int = 5
    pasillo: Optional[str] = None
    estante: Optional[str] = None
    nivel: Optional[str] = None

class Inventario(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id"), nullable=False, unique=True)
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=5)
    pasillo = Column(String(10), nullable=True)
    estante = Column(String(10), nullable=True)
    nivel = Column(String(10), nullable=True)

    autoparte = relationship("Autoparte", backref="inventario")
