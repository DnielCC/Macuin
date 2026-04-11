import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.rol import Rol
from database.usuario import Usuario
from models.auth import LoginRequest, LoginResponse

router_auth = APIRouter(prefix="/v1/auth", tags=["Autenticación"])


@router_auth.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    email = body.email.strip().lower()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    stored = usuario.password_hash
    if not stored or stored.startswith("SEED_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario sin contraseña configurada",
        )
    try:
        ok = bcrypt.checkpw(
            body.password.encode("utf-8"),
            stored.encode("utf-8"),
        )
    except ValueError:
        ok = False
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    if not rol:
        raise HTTPException(status_code=500, detail="Rol inconsistente")
    return LoginResponse(
        id=usuario.id,
        nombre=usuario.nombre,
        apellidos=usuario.apellidos,
        email=usuario.email,
        rol=rol.nombre_rol,
    )
