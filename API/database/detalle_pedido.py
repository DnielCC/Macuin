from sqlalchemy import Column, Integer, Numeric, ForeignKey, Computed
from sqlalchemy.orm import relationship
from database.db import Base

class DetallePedido(Base):
    __tablename__ = "detalles_pedidos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_historico = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), Computed('cantidad * precio_historico', persisted=True))

    pedido = relationship("Pedido", backref="detalles")
    autoparte = relationship("Autoparte", back_populates="detalles_pedidos")
