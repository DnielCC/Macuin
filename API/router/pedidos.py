from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.autoparte import Autoparte
from database.db import get_db
from database.db_utils import commit_or_raise
from database.detalle_pedido import DetallePedido
from database.pedido import Pedido
from models.detalle_pedido import DetallePedidoLineaCreate
from models.pedido import PedidoBase
from models.pedido_extra import PedidoCancelacionPatch, PedidoEstatusPatch
from security.auth import varificar_peticion

routerped = APIRouter(prefix="/v1/pedidos", tags=["CRUD PEDIDOS"])


@routerped.get("/")
def obtener_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).order_by(Pedido.id.desc()).limit(500).all()


@routerped.get("/{pedido_id}/detalles")
def listar_detalles_pedido(pedido_id: int, db: Session = Depends(get_db)):
    if not db.query(Pedido).filter(Pedido.id == pedido_id).first():
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return (
        db.query(DetallePedido).filter(DetallePedido.pedido_id == pedido_id).all()
    )


@routerped.post(
    "/{pedido_id}/detalles",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(varificar_peticion)],
)
def agregar_detalle_pedido(
    pedido_id: int,
    body: DetallePedidoLineaCreate,
    db: Session = Depends(get_db),
):
    if not db.query(Pedido).filter(Pedido.id == pedido_id).first():
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if not db.query(Autoparte).filter(Autoparte.id == body.autoparte_id).first():
        raise HTTPException(status_code=400, detail="Autoparte no existe")
    d = DetallePedido(
        pedido_id=pedido_id,
        autoparte_id=body.autoparte_id,
        cantidad=body.cantidad,
        precio_historico=body.precio_historico,
    )
    db.add(d)
    commit_or_raise(db)
    db.refresh(d)
    return d


@routerped.delete(
    "/{pedido_id}/detalles/{detalle_id}",
    dependencies=[Depends(varificar_peticion)],
)
def eliminar_detalle_pedido(pedido_id: int, detalle_id: int, db: Session = Depends(get_db)):
    d = (
        db.query(DetallePedido)
        .filter(
            DetallePedido.id == detalle_id,
            DetallePedido.pedido_id == pedido_id,
        )
        .first()
    )
    if not d:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    db.delete(d)
    commit_or_raise(db)
    return {"ok": True}


@routerped.get("/{pedido_id}")
def obtener_pedido_por_id(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@routerped.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_pedido(pedido: PedidoBase, db: Session = Depends(get_db)):
    nuevo_pedido = Pedido(**pedido.model_dump())
    db.add(nuevo_pedido)
    commit_or_raise(db)
    db.refresh(nuevo_pedido)
    return nuevo_pedido


@routerped.put("/{pedido_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_pedido(pedido_id: int, pedido_actualizado: PedidoBase, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for key, value in pedido_actualizado.model_dump().items():
        setattr(pedido, key, value)
    commit_or_raise(db)
    db.refresh(pedido)
    return pedido


@routerped.patch("/{pedido_id}/estatus", dependencies=[Depends(varificar_peticion)])
def patch_estatus_pedido(
    pedido_id: int,
    body: PedidoEstatusPatch,
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido.estatus_id = body.estatus_id
    commit_or_raise(db)
    db.refresh(pedido)
    return pedido


@routerped.patch("/{pedido_id}/cancelar", dependencies=[Depends(varificar_peticion)])
def cancelar_pedido(
    pedido_id: int,
    body: PedidoCancelacionPatch,
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido.motivo_cancelacion = body.motivo_cancelacion
    pedido.fecha_cancelacion = body.fecha_cancelacion or datetime.now(timezone.utc)
    commit_or_raise(db)
    db.refresh(pedido)
    return pedido


@routerped.delete("/{pedido_id}", dependencies=[Depends(varificar_peticion)])
def borrar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(pedido)
    commit_or_raise(db)
    return {"mensaje": "Pedido eliminado"}
