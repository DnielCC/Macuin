from typing import Optional
from pydantic import BaseModel

class PedidoBase(BaseModel):
    folio: Optional[str] = None
    usuario_id: int
    estatus_id: int
    total: float = 0.00
    direccion_envio_id: int