from typing import Optional

from pydantic import BaseModel


class CarritoCreate(BaseModel):
    """Si no envías uuid, el servidor genera uno."""

    uuid: Optional[str] = None
    laravel_user_id: Optional[int] = None
    email_invitado: Optional[str] = None


class CarritoLineaCreate(BaseModel):
    autoparte_id: int
    cantidad: int
    precio_unitario: float
