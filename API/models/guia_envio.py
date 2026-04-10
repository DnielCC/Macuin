from typing import Optional

from pydantic import BaseModel


class GuiaEnvioBase(BaseModel):
    pedido_id: int
    tipo: str
    paqueteria: str
    numero_rastreo: Optional[str] = None
    peso_kg: Optional[float] = None
    servicio: Optional[str] = None
    notas_entrega: Optional[str] = None
    archivo_url: Optional[str] = None


class GuiaEnvioUpdate(BaseModel):
    tipo: Optional[str] = None
    paqueteria: Optional[str] = None
    numero_rastreo: Optional[str] = None
    peso_kg: Optional[float] = None
    servicio: Optional[str] = None
    notas_entrega: Optional[str] = None
    archivo_url: Optional[str] = None
