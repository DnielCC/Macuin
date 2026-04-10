from typing import Optional
from pydantic import BaseModel

class DireccionBase(BaseModel):
    calle_principal: str
    num_ext: str
    num_int: Optional[str] = None
    colonia: str
    municipio: str
    estado: str
    cp: str
    referencias: Optional[str] = None
    cliente_id: Optional[int] = None
