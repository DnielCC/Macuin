from typing import Optional
from pydantic import BaseModel

class RolBase(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None
    permisos: Optional[str] = None
