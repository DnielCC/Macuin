from pydantic import BaseModel

class AutoparteBase(BaseModel):
    sku: str
    nombre: str
    precio: float
    stock: int