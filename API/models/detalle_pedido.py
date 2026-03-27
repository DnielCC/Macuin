from pydantic import BaseModel

class DetallePedidoBase(BaseModel):
    pedido_id: int
    autoparte_id: int
    cantidad: int
    precio_historico: float
