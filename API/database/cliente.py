from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database.db import Base


class Cliente(Base):
    """Clientes B2B (módulo Ventas Flask) y referencia para pedidos."""

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    telefono = Column(String(30), nullable=True)
    activo = Column(Boolean, default=True)
    notas = Column(Text, nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
