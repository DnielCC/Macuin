from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.estatus_pedido import EstatusPedido
from models.estatus_pedido import EstatusPedidoBase
from security.auth import varificar_peticion

router_estatus = APIRouter(prefix="/v1/estatus-pedido", tags=["Estatus de pedido"])


@router_estatus.get("/")
def listar_estatus(db: Session = Depends(get_db)):
    return db.query(EstatusPedido).order_by(EstatusPedido.id).all()


@router_estatus.get("/{estatus_id}")
def obtener_estatus(estatus_id: int, db: Session = Depends(get_db)):
    e = db.query(EstatusPedido).filter(EstatusPedido.id == estatus_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Estatus no encontrado")
    return e


@router_estatus.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_estatus(body: EstatusPedidoBase, db: Session = Depends(get_db)):
    e = EstatusPedido(**body.model_dump())
    db.add(e)
    commit_or_raise(db)
    db.refresh(e)
    return e


@router_estatus.put("/{estatus_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_estatus(estatus_id: int, body: EstatusPedidoBase, db: Session = Depends(get_db)):
    e = db.query(EstatusPedido).filter(EstatusPedido.id == estatus_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Estatus no encontrado")
    for k, v in body.model_dump().items():
        setattr(e, k, v)
    commit_or_raise(db)
    db.refresh(e)
    return e


@router_estatus.delete("/{estatus_id}", dependencies=[Depends(varificar_peticion)])
def eliminar_estatus(estatus_id: int, db: Session = Depends(get_db)):
    e = db.query(EstatusPedido).filter(EstatusPedido.id == estatus_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Estatus no encontrado")
    db.delete(e)
    commit_or_raise(db)
    return {"ok": True}
