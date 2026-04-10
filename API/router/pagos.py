from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.carrito import Carrito
from database.db import get_db
from database.db_utils import commit_or_raise
from database.pago import Pago
from database.pedido import Pedido
from models.pago import PagoCreate
from security.auth import varificar_peticion

router_pagos = APIRouter(prefix="/v1/pagos", tags=["Pagos"])


@router_pagos.get("/")
def listar_pagos(db: Session = Depends(get_db), limite: int = 100):
    return db.query(Pago).order_by(Pago.id.desc()).limit(min(limite, 500)).all()


@router_pagos.get("/{pago_id}")
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    p = db.query(Pago).filter(Pago.id == pago_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return p


@router_pagos.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_pago(body: PagoCreate, db: Session = Depends(get_db)):
    if body.pedido_id and not db.query(Pedido).filter(Pedido.id == body.pedido_id).first():
        raise HTTPException(status_code=400, detail="Pedido no existe")
    if body.carrito_id and not db.query(Carrito).filter(Carrito.id == body.carrito_id).first():
        raise HTTPException(status_code=400, detail="Carrito no existe")
    if not body.pedido_id and not body.carrito_id:
        raise HTTPException(
            status_code=400,
            detail="Debe indicarse pedido_id o carrito_id.",
        )
    p = Pago(**body.model_dump())
    db.add(p)
    commit_or_raise(db)
    db.refresh(p)
    return p
