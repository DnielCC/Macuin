from typing import Optional
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    email: str
    password_hash: str
    telefono: Optional[str] = None
    rol_id: int
    direccion_id: Optional[int] = None
    activo: bool = True