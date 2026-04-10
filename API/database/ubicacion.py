from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base


class Ubicacion(Base):
    """Ubicaciones físicas de almacén (pasillo / estante / capacidad)."""

    __tablename__ = "ubicaciones"

    id = Column(Integer, primary_key=True, index=True)
    pasillo = Column(String(20), nullable=False)
    estante = Column(String(20), nullable=False)
    nivel = Column(String(10), nullable=True)
    capacidad = Column(Integer, nullable=True)
    descripcion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
