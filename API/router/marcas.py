from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from models.marca import MarcaBase
from security.auth import varificar_peticion
from database.db import get_db
from database.marca import Marca
from sqlalchemy.orm import Session

routermarca = APIRouter(
    prefix = "/v1/marcas",
    tags = ["CRUD MARCAS"]
)

@routermarca.get("/")
def obtener_marcas(db: Session = Depends(get_db)):
    return db.query(Marca).all()

@routermarca.get("/{marca_id}")
def obtener_marca_por_id(marca_id: int, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca

@routermarca.post("/")
def crear_marca(marca: MarcaBase, db: Session = Depends(get_db)):
    nueva_marca = Marca(**marca.model_dump())
    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)
    return {"mensaje": "Marca creada", "marca": nueva_marca}

@routermarca.put("/{marca_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_marca(marca_id: int, marca_actualizada: MarcaBase, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    for key, value in marca_actualizada.model_dump().items():
        setattr(marca, key, value)
    db.commit()
    db.refresh(marca)
    return {"mensaje": "Marca actualizada", "marca": marca}

@routermarca.delete("/{marca_id}", dependencies=[Depends(varificar_peticion)])
def borrar_marca(marca_id: int, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    db.delete(marca)
    db.commit()
    return {"mensaje": "Marca eliminada"}
