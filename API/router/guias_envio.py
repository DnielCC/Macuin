from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.guia_envio import GuiaEnvio
from database.pedido import Pedido
from models.guia_envio import GuiaEnvioBase, GuiaEnvioUpdate
from security.auth import varificar_peticion

router_guias = APIRouter(prefix="/v1/guias-envio", tags=["Guías de envío"])


@router_guias.get("/")
def listar_guias(db: Session = Depends(get_db)):
    return db.query(GuiaEnvio).order_by(GuiaEnvio.id.desc()).limit(500).all()


@router_guias.get("/pedido/{pedido_id}")
def listar_guias_por_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return db.query(GuiaEnvio).filter(GuiaEnvio.pedido_id == pedido_id).all()


@router_guias.get("/{guia_id}")
def obtener_guia(guia_id: int, db: Session = Depends(get_db)):
    g = db.query(GuiaEnvio).filter(GuiaEnvio.id == guia_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Guía no encontrada")
    return g


@router_guias.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_guia(body: GuiaEnvioBase, db: Session = Depends(get_db)):
    if not db.query(Pedido).filter(Pedido.id == body.pedido_id).first():
        raise HTTPException(status_code=400, detail="Pedido no existe")
    g = GuiaEnvio(**body.model_dump())
    db.add(g)
    commit_or_raise(db)
    db.refresh(g)
    return g


@router_guias.put("/{guia_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_guia(guia_id: int, body: GuiaEnvioUpdate, db: Session = Depends(get_db)):
    g = db.query(GuiaEnvio).filter(GuiaEnvio.id == guia_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Guía no encontrada")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(g, k, v)
    commit_or_raise(db)
    db.refresh(g)
    return g


@router_guias.delete("/{guia_id}", dependencies=[Depends(varificar_peticion)])
def eliminar_guia(guia_id: int, db: Session = Depends(get_db)):
    g = db.query(GuiaEnvio).filter(GuiaEnvio.id == guia_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Guía no encontrada")
    db.delete(g)
    commit_or_raise(db)
    return {"ok": True}
