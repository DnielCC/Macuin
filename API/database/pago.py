from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base


class Pago(Base):
    """Registro de intentos y resultados de pago (portal Laravel / checkout)."""

    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="SET NULL"), nullable=True, index=True)
    carrito_id = Column(Integer, ForeignKey("carritos.id", ondelete="SET NULL"), nullable=True, index=True)
    monto = Column(Numeric(15, 2), nullable=False)
    moneda = Column(String(3), nullable=False, default="MXN")
    estado = Column(String(30), nullable=False, default="pendiente")
    pasarela = Column(String(80), nullable=True)
    referencia_externa = Column(String(120), nullable=True)
    respuesta_proveedor = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    pedido = relationship("Pedido", backref="pagos")
    carrito = relationship("Carrito", backref="pagos")
