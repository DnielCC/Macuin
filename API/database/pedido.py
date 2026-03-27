from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String(20), unique=True, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estatus_id = Column(Integer, ForeignKey("estatus_pedido.id"), nullable=False)
    total = Column(Numeric(15, 2), default=0.00)
    direccion_envio_id = Column(Integer, ForeignKey("direcciones.id"), nullable=False)
    fecha_pedido = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario = relationship("Usuario", backref="pedidos")
    estatus = relationship("EstatusPedido", backref="pedidos")
    direccion_envio = relationship("Direccion", backref="pedidos")
