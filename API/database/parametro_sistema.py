from sqlalchemy import Column, Integer, String, Boolean, Text, UniqueConstraint
from database.db import Base


class ParametroSistema(Base):
    """Parámetros generales y metadatos de configuración (módulo Admin)."""

    __tablename__ = "parametros_sistema"

    __table_args__ = (UniqueConstraint("tipo", "clave", name="uq_parametro_tipo_clave"),)

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(40), nullable=False, index=True)
    clave = Column(String(120), nullable=False)
    valor = Column(Text, nullable=False)
    descripcion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
