from pydantic import BaseModel

#VALIDACIÓN PYDADNTIC
class PedidoBase(BaseModel):
    usuario_id: int
    total: float
    estatus: str