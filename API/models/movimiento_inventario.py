from typing import Optional

from pydantic import BaseModel, Field


class MovimientoInventarioCreate(BaseModel):
    tipo: str = Field(..., pattern="^(entrada|merma)$")
    cantidad: int = Field(..., gt=0)
    notas: Optional[str] = None
    usuario_id: Optional[int] = None
