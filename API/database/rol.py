from sqlalchemy import Column, Integer, String, Text
from database.db import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(30), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    permisos = Column(String(500), nullable=True)
