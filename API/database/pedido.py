from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
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
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True, index=True)
    motivo_cancelacion = Column(Text, nullable=True)
    fecha_cancelacion = Column(DateTime(timezone=True), nullable=True)
    fecha_pedido = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario = relationship("Usuario", backref="pedidos")
    estatus = relationship("EstatusPedido", backref="pedidos")
    direccion_envio = relationship("Direccion", backref="pedidos")
    cliente = relationship("Cliente", backref="pedidos")
    guias = relationship(
        "GuiaEnvio",
        back_populates="pedido",
        cascade="all, delete-orphan",
    )
