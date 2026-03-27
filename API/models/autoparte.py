from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

class AutoparteBase(BaseModel):
    sku_codigo: str
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: float
    imagen_url: Optional[str] = None
    categoria_id: int
    marca_id: int

class Autoparte(Base):
    __tablename__ = "autopartes"

    id = Column(Integer, primary_key=True, index=True)
    sku_codigo = Column(String(50), nullable=False, unique=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    marca_id = Column(Integer, ForeignKey("marcas.id"), nullable=False)
    fecha_alta = Column(DateTime(timezone=True), server_default=func.now())

    categoria = relationship("Categoria", backref="autopartes")
    marca = relationship("Marca", backref="autopartes")