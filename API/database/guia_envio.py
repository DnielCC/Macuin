from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base


class GuiaEnvio(Base):
    """Guías de envío / etiquetas (módulo Logística)."""

    __tablename__ = "guias_envio"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo = Column(String(20), nullable=False)
    paqueteria = Column(String(80), nullable=False)
    numero_rastreo = Column(String(120), nullable=True)
    peso_kg = Column(Numeric(10, 2), nullable=True)
    servicio = Column(String(80), nullable=True)
    notas_entrega = Column(Text, nullable=True)
    archivo_url = Column(String(500), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    pedido = relationship("Pedido", back_populates="guias")
