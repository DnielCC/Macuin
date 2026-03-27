from typing import Optional
from pydantic import BaseModel

class InventarioBase(BaseModel):
    autoparte_id: int
    stock_actual: int = 0
    stock_minimo: int = 5
    pasillo: Optional[str] = None
    estante: Optional[str] = None
    nivel: Optional[str] = None
