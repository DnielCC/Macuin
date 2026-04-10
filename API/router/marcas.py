from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.marca import Marca
from models.marca import MarcaBase
from security.auth import varificar_peticion

routermarca = APIRouter(prefix="/v1/marcas", tags=["CRUD MARCAS"])


@routermarca.get("/")
def obtener_marcas(db: Session = Depends(get_db)):
    return db.query(Marca).order_by(Marca.id).all()


@routermarca.get("/{marca_id}")
def obtener_marca_por_id(marca_id: int, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca


@routermarca.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_marca(marca: MarcaBase, db: Session = Depends(get_db)):
    nueva_marca = Marca(**marca.model_dump())
    db.add(nueva_marca)
    commit_or_raise(db)
    db.refresh(nueva_marca)
    return nueva_marca


@routermarca.put("/{marca_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_marca(marca_id: int, marca_actualizada: MarcaBase, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    for key, value in marca_actualizada.model_dump().items():
        setattr(marca, key, value)
    commit_or_raise(db)
    db.refresh(marca)
    return marca


@routermarca.delete("/{marca_id}", dependencies=[Depends(varificar_peticion)])
def borrar_marca(marca_id: int, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    db.delete(marca)
    commit_or_raise(db)
    return {"mensaje": "Marca eliminada"}
