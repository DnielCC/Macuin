from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Inventario(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id"), nullable=False, unique=True)
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True, index=True)
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=5)
    pasillo = Column(String(10), nullable=True)
    estante = Column(String(10), nullable=True)
    nivel = Column(String(10), nullable=True)

    autoparte = relationship("Autoparte", backref="inventario")
    ubicacion = relationship("Ubicacion", backref="inventarios")
    movimientos = relationship(
        "MovimientoInventario",
        back_populates="inventario",
        cascade="all, delete-orphan",
    )
