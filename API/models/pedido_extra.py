from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PedidoEstatusPatch(BaseModel):
    estatus_id: int


class PedidoCancelacionPatch(BaseModel):
    motivo_cancelacion: str = Field(..., min_length=1)
    fecha_cancelacion: Optional[datetime] = None
