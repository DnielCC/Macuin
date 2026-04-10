from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.rol import Rol
from models.rol import RolBase
from security.auth import varificar_peticion

routerrol = APIRouter(prefix="/v1/roles", tags=["CRUD ROLES"])


@routerrol.get("/")
def obtener_roles(db: Session = Depends(get_db)):
    return db.query(Rol).order_by(Rol.id).all()


@routerrol.get("/{rol_id}")
def obtener_rol_por_id(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@routerrol.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_rol(rol: RolBase, db: Session = Depends(get_db)):
    nuevo_rol = Rol(**rol.model_dump())
    db.add(nuevo_rol)
    commit_or_raise(db)
    db.refresh(nuevo_rol)
    return nuevo_rol


@routerrol.put("/{rol_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_rol(rol_id: int, rol_actualizado: RolBase, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    for key, value in rol_actualizado.model_dump().items():
        setattr(rol, key, value)
    commit_or_raise(db)
    db.refresh(rol)
    return rol


@routerrol.delete("/{rol_id}", dependencies=[Depends(varificar_peticion)])
def borrar_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(rol)
    commit_or_raise(db)
    return {"mensaje": "Rol eliminado"}
