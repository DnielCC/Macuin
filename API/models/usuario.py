from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    email: str
    password_hash: str
    telefono: Optional[str] = None
    rol_id: int
    direccion_id: Optional[int] = None
    activo: bool = True

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    rol = relationship("Rol", backref="usuarios")
    direccion = relationship("Direccion", backref="usuarios")