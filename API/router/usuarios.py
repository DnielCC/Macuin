from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from models.usuario import UsuarioBase
from security.auth import varificar_peticion
from database.db import get_db
from database.usuario import Usuario
from sqlalchemy.orm import Session

routerusu = APIRouter(
    prefix = "/v1/usuarios",
    tags = ["CRUD USUARIOS"]
)

#1- todos los usuarios
@routerusu.get("/")
def leer_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status":"200"
    }

#2- usuario por id
@routerusu.get("/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

#3- crear usuario
@routerusu.post("/")
def crear_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario creado", "usuario": nuevo_usuario}

#4- Modificar usuario
@routerusu.put("/{usuario_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_usuario(usuario_id: int, usuario_actualizado: UsuarioBase, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario_actualizado.model_dump().items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Usuario actualizado", "usuario": usuario}

#5- eliminar usuario
@routerusu.delete("/{usuario_id}", dependencies=[Depends(varificar_peticion)])
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}