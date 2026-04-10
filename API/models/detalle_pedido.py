from pydantic import BaseModel, Field


class DetallePedidoBase(BaseModel):
    pedido_id: int
    autoparte_id: int
    cantidad: int
    precio_historico: float


class DetallePedidoLineaCreate(BaseModel):
    autoparte_id: int
    cantidad: int = Field(..., gt=0)
    precio_historico: float = Field(..., ge=0)
