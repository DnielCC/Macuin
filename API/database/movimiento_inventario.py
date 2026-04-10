from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base


class MovimientoInventario(Base):
    """Entradas y mermas de stock (módulo Almacén)."""

    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    inventario_id = Column(Integer, ForeignKey("inventarios.id"), nullable=False, index=True)
    tipo = Column(String(20), nullable=False)
    cantidad = Column(Integer, nullable=False)
    notas = Column(Text, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    inventario = relationship("Inventario", back_populates="movimientos")
    usuario = relationship("Usuario", backref="movimientos_inventario")
