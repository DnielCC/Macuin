from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database.db import Base

class MarcaBase(BaseModel):
    nombre: str

class Marca(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
