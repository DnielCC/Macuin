from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.categoria import Categoria
from database.db import get_db
from database.db_utils import commit_or_raise
from models.categoria import CategoriaBase
from security.auth import varificar_peticion

routercat = APIRouter(prefix="/v1/categorias", tags=["CRUD CATEGORIAS"])


@routercat.get("/")
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).order_by(Categoria.id).all()


@routercat.get("/{categoria_id}")
def obtener_categoria_por_id(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria


@routercat.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_categoria(categoria: CategoriaBase, db: Session = Depends(get_db)):
    nueva_categoria = Categoria(**categoria.model_dump())
    db.add(nueva_categoria)
    commit_or_raise(db)
    db.refresh(nueva_categoria)
    return nueva_categoria


@routercat.put("/{categoria_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_categoria(categoria_id: int, categoria_actualizada: CategoriaBase, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    for key, value in categoria_actualizada.model_dump().items():
        setattr(categoria, key, value)
    commit_or_raise(db)
    db.refresh(categoria)
    return categoria


@routercat.delete("/{categoria_id}", dependencies=[Depends(varificar_peticion)])
def borrar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    db.delete(categoria)
    commit_or_raise(db)
    return {"mensaje": "Categoria eliminada"}
