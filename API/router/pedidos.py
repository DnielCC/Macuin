from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from database.autoparte import Autoparte
from database.cliente import Cliente
from database.db import get_db
from database.db_utils import commit_or_raise
from database.detalle_pedido import DetallePedido
from database.direccion import Direccion
from database.estatus_pedido import EstatusPedido
from database.pedido import Pedido
from models.detalle_pedido import DetallePedidoLineaCreate
from models.pedido import PedidoBase
from models.pedido_extra import PedidoCancelacionPatch, PedidoEstatusPatch
from security.auth import varificar_peticion

routerped = APIRouter(prefix="/v1/pedidos", tags=["CRUD PEDIDOS"])


@routerped.get("/")
def obtener_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).order_by(Pedido.id.desc()).limit(500).all()


@routerped.get("/admin/vista")
def pedidos_admin_vista(
    limit: int = Query(300, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Listado enriquecido para panel Admin (Flask): cliente, destino, piezas, estatus."""
    piezas_sq = (
        db.query(
            DetallePedido.pedido_id.label("pedido_id"),
            sa_func.coalesce(sa_func.sum(DetallePedido.cantidad), 0).label("piezas"),
        )
        .group_by(DetallePedido.pedido_id)
        .subquery()
    )
    rows = (
        db.query(Pedido, Cliente, Direccion, EstatusPedido, piezas_sq.c.piezas)
        .outerjoin(Cliente, Pedido.cliente_id == Cliente.id)
        .outerjoin(Direccion, Pedido.direccion_envio_id == Direccion.id)
        .join(EstatusPedido, Pedido.estatus_id == EstatusPedido.id)
        .outerjoin(piezas_sq, piezas_sq.c.pedido_id == Pedido.id)
        .order_by(Pedido.id.desc())
        .limit(limit)
        .all()
    )
    out = []
    for ped, cli, dire, est, piezas in rows:
        dest = "—"
        if dire is not None:
            m, e = (dire.municipio or "").strip(), (dire.estado or "").strip()
            dest = ", ".join(x for x in (m, e) if x) or "—"
        fp = ped.fecha_pedido
        out.append(
            {
                "id": ped.id,
                "folio": ped.folio,
                "total": float(ped.total or 0),
                "cliente_nombre": (cli.nombre if cli else None) or "—",
                "destino": dest,
                "piezas": int(piezas or 0),
                "estatus": est.nombre,
                "estatus_modulo": (est.modulo or "").strip() or "—",
                "fecha_pedido": fp.isoformat() if fp else None,
                "motivo_cancelacion": ped.motivo_cancelacion,
            }
        )
    return out


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

    # Buscar estatus "Cancelado" para actualizar el estatus_id del pedido
    estatus_cancelado = (
        db.query(EstatusPedido)
        .filter(EstatusPedido.nombre == "Cancelado")
        .first()
    )
    if estatus_cancelado:
        pedido.estatus_id = estatus_cancelado.id

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
