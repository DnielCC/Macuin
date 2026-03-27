from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from models.categoria import CategoriaBase
from security.auth import varificar_peticion
from database.db import get_db
from database.categoria import Categoria
from sqlalchemy.orm import Session

routercat = APIRouter(
    prefix = "/v1/categorias",
    tags = ["CRUD CATEGORIAS"]
)

@routercat.get("/")
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@routercat.get("/{categoria_id}")
def obtener_categoria_por_id(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

@routercat.post("/")
def crear_categoria(categoria: CategoriaBase, db: Session = Depends(get_db)):
    nueva_categoria = Categoria(**categoria.model_dump())
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return {"mensaje": "Categoria creada", "categoria": nueva_categoria}

@routercat.put("/{categoria_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_categoria(categoria_id: int, categoria_actualizada: CategoriaBase, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    for key, value in categoria_actualizada.model_dump().items():
        setattr(categoria, key, value)
    db.commit()
    db.refresh(categoria)
    return {"mensaje": "Categoria actualizada", "categoria": categoria}

@routercat.delete("/{categoria_id}", dependencies=[Depends(varificar_peticion)])
def borrar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoria eliminada"}
