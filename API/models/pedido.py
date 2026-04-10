from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PedidoBase(BaseModel):
    folio: Optional[str] = None
    usuario_id: int
    estatus_id: int
    total: float = 0.00
    direccion_envio_id: int
    cliente_id: Optional[int] = None
    motivo_cancelacion: Optional[str] = None
    fecha_cancelacion: Optional[datetime] = None