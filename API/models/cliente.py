from typing import Optional
from pydantic import BaseModel


class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    activo: bool = True
    notas: Optional[str] = None
