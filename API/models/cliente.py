from typing import Optional

from pydantic import BaseModel


class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    activo: bool = True
    notas: Optional[str] = None


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
    notas: Optional[str] = None
