from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database.db import Base

class RolBase(BaseModel):
    nombre_rol: str

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(30), nullable=False, unique=True)
