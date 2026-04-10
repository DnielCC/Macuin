from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.usuario import Usuario
from models.usuario import UsuarioBase
from security.auth import varificar_peticion

routerusu = APIRouter(prefix="/v1/usuarios", tags=["CRUD USUARIOS"])


@routerusu.get("/")
def leer_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return {"total": len(usuarios), "usuarios": usuarios}


@routerusu.get("/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@routerusu.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    commit_or_raise(db)
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@routerusu.put("/{usuario_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_usuario(usuario_id: int, usuario_actualizado: UsuarioBase, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario_actualizado.model_dump().items():
        setattr(usuario, key, value)
    commit_or_raise(db)
    db.refresh(usuario)
    return usuario


@routerusu.delete("/{usuario_id}", dependencies=[Depends(varificar_peticion)])
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    commit_or_raise(db)
    return {"mensaje": "Usuario eliminado correctamente"}
