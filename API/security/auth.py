import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

_API_USER = os.getenv("API_BASIC_USER", "alidaniel")
_API_PASS = os.getenv("API_BASIC_PASSWORD", "123456")


def varificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    """HTTP Basic para operaciones de escritura (FASE 2). Credenciales por entorno en Docker."""
    usuario_correcto = secrets.compare_digest(credentials.username, _API_USER)
    contrasena_correcta = secrets.compare_digest(credentials.password, _API_PASS)

    if not (usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
    return credentials.username