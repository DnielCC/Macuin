from typing import Optional

from pydantic import BaseModel


class PagoCreate(BaseModel):
    pedido_id: Optional[int] = None
    carrito_id: Optional[int] = None
    monto: float
    moneda: str = "MXN"
    estado: str = "pendiente"
    pasarela: Optional[str] = None
    referencia_externa: Optional[str] = None
    respuesta_proveedor: Optional[str] = None
