from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from models.inventario import InventarioBase
from security.auth import varificar_peticion
from database.db import get_db
from database.inventario import Inventario
from sqlalchemy.orm import Session

routerinv = APIRouter(
    prefix = "/v1/inventarios",
    tags = ["HTTP CRUD"]
)

@routerinv.get("/")
def obtener_inventarios(db: Session = Depends(get_db)):
    return db.query(Inventario).all()

@routerinv.get("/{inventario_id}")
def obtener_inventario_por_id(inventario_id: int, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

@routerinv.post("/")
def crear_inventario(inventario: InventarioBase, db: Session = Depends(get_db)):
    nuevo_inventario = Inventario(**inventario.model_dump())
    db.add(nuevo_inventario)
    db.commit()
    db.refresh(nuevo_inventario)
    return {"mensaje": "Inventario creado", "inventario": nuevo_inventario}

@routerinv.put("/{inventario_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_inventario(inventario_id: int, inventario_actualizado: InventarioBase, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    for key, value in inventario_actualizado.model_dump().items():
        setattr(inventario, key, value)
    db.commit()
    db.refresh(inventario)
    return {"mensaje": "Inventario actualizado", "inventario": inventario}

@routerinv.delete("/{inventario_id}", dependencies=[Depends(varificar_peticion)])
def borrar_inventario(inventario_id: int, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    db.delete(inventario)
    db.commit()
    return {"mensaje": "Inventario eliminado"}
