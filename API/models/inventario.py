from typing import Optional
from pydantic import BaseModel

class InventarioBase(BaseModel):
    autoparte_id: int
    ubicacion_id: Optional[int] = None
    stock_actual: int = 0
    stock_minimo: int = 5
    pasillo: Optional[str] = None
    estante: Optional[str] = None
    nivel: Optional[str] = None
