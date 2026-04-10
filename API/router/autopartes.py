from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database.autoparte import Autoparte
from database.db import get_db
from database.db_utils import commit_or_raise
from models.autoparte import AutoparteBase
from security.auth import varificar_peticion

routerauto = APIRouter(prefix="/v1/autopartes", tags=["CRUD AUTOPARTES"])


@routerauto.get("/buscar")
def buscar_autoparte_por_nombre(nombre: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    resultados = db.query(Autoparte).filter(Autoparte.nombre.ilike(f"%{nombre}%")).all()
    if not resultados:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron autopartes con ese nombre",
        )
    return resultados


@routerauto.get("/")
def obtener_autopartes(db: Session = Depends(get_db)):
    return db.query(Autoparte).order_by(Autoparte.id).all()


@routerauto.get("/{autoparte_id}")
def obtener_autoparte(autoparte_id: int, db: Session = Depends(get_db)):
    autoparte = db.query(Autoparte).filter(Autoparte.id == autoparte_id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return autoparte


@routerauto.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_autoparte(autoparte: AutoparteBase, db: Session = Depends(get_db)):
    nueva = Autoparte(**autoparte.model_dump())
    db.add(nueva)
    commit_or_raise(db)
    db.refresh(nueva)
    return nueva


@routerauto.put("/{autoparte_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_autoparte(autoparte_id: int, auto_act: AutoparteBase, db: Session = Depends(get_db)):
    autoparte = db.query(Autoparte).filter(Autoparte.id == autoparte_id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    for key, value in auto_act.model_dump().items():
        setattr(autoparte, key, value)
    commit_or_raise(db)
    db.refresh(autoparte)
    return autoparte


@routerauto.delete("/{autoparte_id}", dependencies=[Depends(varificar_peticion)])
def borrar_autoparte(autoparte_id: int, db: Session = Depends(get_db)):
    autoparte = db.query(Autoparte).filter(Autoparte.id == autoparte_id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    db.delete(autoparte)
    commit_or_raise(db)
    return {"mensaje": "Autoparte eliminada"}
