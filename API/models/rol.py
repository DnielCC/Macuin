from pydantic import BaseModel

class RolBase(BaseModel):
    nombre_rol: str
