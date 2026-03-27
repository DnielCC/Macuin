from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from database.db import Base

class DireccionBase(BaseModel):
    calle_principal: str
    num_ext: str
    num_int: Optional[str] = None
    colonia: str
    municipio: str
    estado: str
    cp: str
    referencias: Optional[str] = None

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
