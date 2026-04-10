from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.direccion import Direccion
from models.direccion import DireccionBase
from security.auth import varificar_peticion

routerdir = APIRouter(prefix="/v1/direcciones", tags=["CRUD DIRECCIONES"])


@routerdir.get("/")
def obtener_direcciones(db: Session = Depends(get_db)):
    return db.query(Direccion).order_by(Direccion.id).all()


@routerdir.get("/{direccion_id}")
def obtener_direccion_por_id(direccion_id: int, db: Session = Depends(get_db)):
    direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
    if not direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    return direccion


@routerdir.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_direccion(direccion: DireccionBase, db: Session = Depends(get_db)):
    nueva_direccion = Direccion(**direccion.model_dump())
    db.add(nueva_direccion)
    commit_or_raise(db)
    db.refresh(nueva_direccion)
    return nueva_direccion


@routerdir.put("/{direccion_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_direccion(direccion_id: int, direccion_actualizada: DireccionBase, db: Session = Depends(get_db)):
    direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
    if not direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    for key, value in direccion_actualizada.model_dump().items():
        setattr(direccion, key, value)
    commit_or_raise(db)
    db.refresh(direccion)
    return direccion


@routerdir.delete("/{direccion_id}", dependencies=[Depends(varificar_peticion)])
def borrar_direccion(direccion_id: int, db: Session = Depends(get_db)):
    direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
    if not direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    db.delete(direccion)
    commit_or_raise(db)
    return {"mensaje": "Direccion eliminada"}
