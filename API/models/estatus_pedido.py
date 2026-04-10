from typing import Optional
from pydantic import BaseModel

class EstatusPedidoBase(BaseModel):
    nombre: str
    modulo: Optional[str] = None
    color: Optional[str] = None
