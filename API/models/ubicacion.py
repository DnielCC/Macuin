from typing import Optional

from pydantic import BaseModel


class UbicacionBase(BaseModel):
    pasillo: str
    estante: str
    nivel: Optional[str] = None
    capacidad: Optional[int] = None
    descripcion: Optional[str] = None
    activo: bool = True


class UbicacionUpdate(BaseModel):
    pasillo: Optional[str] = None
    estante: Optional[str] = None
    nivel: Optional[str] = None
    capacidad: Optional[int] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
