from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.inventario import Inventario
from models.inventario import InventarioBase
from security.auth import varificar_peticion

routerinv = APIRouter(prefix="/v1/inventarios", tags=["CRUD INVENTARIOS"])


@routerinv.get("/")
def obtener_inventarios(db: Session = Depends(get_db)):
    return db.query(Inventario).order_by(Inventario.id).all()


@routerinv.get("/{inventario_id}")
def obtener_inventario_por_id(inventario_id: int, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario


@routerinv.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_inventario(inventario: InventarioBase, db: Session = Depends(get_db)):
    nuevo_inventario = Inventario(**inventario.model_dump())
    db.add(nuevo_inventario)
    commit_or_raise(db)
    db.refresh(nuevo_inventario)
    return nuevo_inventario


@routerinv.put("/{inventario_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_inventario(inventario_id: int, inventario_actualizado: InventarioBase, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    for key, value in inventario_actualizado.model_dump().items():
        setattr(inventario, key, value)
    commit_or_raise(db)
    db.refresh(inventario)
    return inventario


@routerinv.delete("/{inventario_id}", dependencies=[Depends(varificar_peticion)])
def borrar_inventario(inventario_id: int, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    db.delete(inventario)
    commit_or_raise(db)
    return {"mensaje": "Inventario eliminado"}
