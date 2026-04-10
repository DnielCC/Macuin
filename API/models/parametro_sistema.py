from typing import Optional

from pydantic import BaseModel


class ParametroSistemaBase(BaseModel):
    tipo: str
    clave: str
    valor: str
    descripcion: Optional[str] = None
    activo: bool = True


class ParametroSistemaUpdate(BaseModel):
    valor: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
