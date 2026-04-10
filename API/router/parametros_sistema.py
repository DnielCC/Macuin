from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.parametro_sistema import ParametroSistema
from models.parametro_sistema import ParametroSistemaBase, ParametroSistemaUpdate
from security.auth import varificar_peticion

router_parametros = APIRouter(prefix="/v1/parametros-sistema", tags=["Parámetros de sistema"])


@router_parametros.get("/")
def listar_parametros(db: Session = Depends(get_db), tipo: Optional[str] = None):
    q = db.query(ParametroSistema)
    if tipo:
        q = q.filter(ParametroSistema.tipo == tipo)
    return q.order_by(ParametroSistema.id).all()


@router_parametros.get("/{parametro_id}")
def obtener_parametro(parametro_id: int, db: Session = Depends(get_db)):
    p = db.query(ParametroSistema).filter(ParametroSistema.id == parametro_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    return p


@router_parametros.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_parametro(body: ParametroSistemaBase, db: Session = Depends(get_db)):
    p = ParametroSistema(**body.model_dump())
    db.add(p)
    commit_or_raise(db)
    db.refresh(p)
    return p


@router_parametros.put("/{parametro_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_parametro(
    parametro_id: int, body: ParametroSistemaUpdate, db: Session = Depends(get_db)
):
    p = db.query(ParametroSistema).filter(ParametroSistema.id == parametro_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    commit_or_raise(db)
    db.refresh(p)
    return p


@router_parametros.delete("/{parametro_id}", dependencies=[Depends(varificar_peticion)])
def eliminar_parametro(parametro_id: int, db: Session = Depends(get_db)):
    p = db.query(ParametroSistema).filter(ParametroSistema.id == parametro_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    db.delete(p)
    commit_or_raise(db)
    return {"ok": True}
