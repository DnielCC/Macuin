from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from models.direccion import DireccionBase
from security.auth import varificar_peticion
from database.db import get_db
from database.direccion import Direccion
from sqlalchemy.orm import Session

routerdir = APIRouter(
    prefix = "/v1/direcciones",
    tags = ["HTTP CRUD"]
)

@routerdir.get("/")
def obtener_direcciones(db: Session = Depends(get_db)):
    return db.query(Direccion).all()

@routerdir.get("/{direccion_id}")
def obtener_direccion_por_id(direccion_id: int, db: Session = Depends(get_db)):
    direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
    if not direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    return direccion

@routerdir.post("/")
def crear_direccion(direccion: DireccionBase, db: Session = Depends(get_db)):
    nueva_direccion = Direccion(**direccion.model_dump())
    db.add(nueva_direccion)
    db.commit()
    db.refresh(nueva_direccion)
    return {"mensaje": "Direccion creada", "direccion": nueva_direccion}

@routerdir.put("/{direccion_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_direccion(direccion_id: int, direccion_actualizada: DireccionBase, db: Session = Depends(get_db)):
    direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
    if not direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    for key, value in direccion_actualizada.model_dump().items():
        setattr(direccion, key, value)
    db.commit()
    db.refresh(direccion)
    return {"mensaje": "Direccion actualizada", "direccion": direccion}

@routerdir.delete("/{direccion_id}", dependencies=[Depends(varificar_peticion)])
def borrar_direccion(direccion_id: int, db: Session = Depends(get_db)):
    direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
    if not direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    db.delete(direccion)
    db.commit()
    return {"mensaje": "Direccion eliminada"}
