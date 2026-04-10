from sqlalchemy import Column, Integer, String
from database.db import Base

class EstatusPedido(Base):
    __tablename__ = "estatus_pedido"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    modulo = Column(String(50), nullable=True)
    color = Column(String(30), nullable=True)
