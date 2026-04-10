from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Direccion(Base):
    __tablename__ = "direcciones"

    id = Column(Integer, primary_key=True, index=True)
    calle_principal = Column(String(150), nullable=False)
    num_ext = Column(String(10), nullable=False)
    num_int = Column(String(10), nullable=True)
    colonia = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    cp = Column(String(10), nullable=False, index=True)
    referencias = Column(Text, nullable=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True, index=True)

    cliente = relationship("Cliente", backref="direcciones")
