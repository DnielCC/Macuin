from typing import Optional
from pydantic import BaseModel

class AutoparteBase(BaseModel):
    sku_codigo: str
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: float
    imagen_url: Optional[str] = None
    categoria_id: int
    marca_id: int