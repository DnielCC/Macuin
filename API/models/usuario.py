from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: str