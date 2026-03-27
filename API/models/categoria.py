from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database.db import Base

class CategoriaBase(BaseModel):
    nombre: str

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
