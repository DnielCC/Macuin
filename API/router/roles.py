from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from models.rol import RolBase
from security.auth import varificar_peticion
from database.db import get_db
from database.rol import Rol
from sqlalchemy.orm import Session

routerrol = APIRouter(
    prefix = "/v1/roles",
    tags = ["HTTP CRUD"]
)

@routerrol.get("/")
def obtener_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

@routerrol.get("/{rol_id}")
def obtener_rol_por_id(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@routerrol.post("/")
def crear_rol(rol: RolBase, db: Session = Depends(get_db)):
    nuevo_rol = Rol(**rol.model_dump())
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return {"mensaje": "Rol creado", "rol": nuevo_rol}

@routerrol.put("/{rol_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_rol(rol_id: int, rol_actualizado: RolBase, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    for key, value in rol_actualizado.model_dump().items():
        setattr(rol, key, value)
    db.commit()
    db.refresh(rol)
    return {"mensaje": "Rol actualizado", "rol": rol}

@routerrol.delete("/{rol_id}", dependencies=[Depends(varificar_peticion)])
def borrar_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(rol)
    db.commit()
    return {"mensaje": "Rol eliminado"}
