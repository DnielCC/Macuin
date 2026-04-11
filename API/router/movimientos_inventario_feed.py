"""Consultas agregadas de movimientos de inventario (panel Almacén)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from database.autoparte import Autoparte
from database.db import get_db
from database.inventario import Inventario
from database.movimiento_inventario import MovimientoInventario

router_mov_feed = APIRouter(
    prefix="/v1/movimientos-inventario",
    tags=["Movimientos de inventario"],
)


@router_mov_feed.get("/recientes")
def movimientos_recientes(
    limit: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(MovimientoInventario, Autoparte.sku_codigo, Autoparte.nombre)
        .join(Inventario, MovimientoInventario.inventario_id == Inventario.id)
        .join(Autoparte, Inventario.autoparte_id == Autoparte.id)
        .order_by(
            MovimientoInventario.creado_en.desc().nulls_last(),
            MovimientoInventario.id.desc(),
        )
        .limit(limit)
        .all()
    )
    out = []
    for mov, sku, nombre in rows:
        ce = mov.creado_en
        out.append(
            {
                "id": mov.id,
                "inventario_id": mov.inventario_id,
                "tipo": mov.tipo,
                "cantidad": mov.cantidad,
                "notas": mov.notas,
                "usuario_id": mov.usuario_id,
                "creado_en": ce.isoformat() if ce is not None else None,
                "sku_codigo": sku,
                "autoparte_nombre": nombre,
            }
        )
    return out


@router_mov_feed.get("/resumen-por-mes")
def resumen_movimientos_por_mes(
    months: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
):
    ym_expr = sa_func.to_char(MovimientoInventario.creado_en, "YYYY-MM")
    rows = (
        db.query(ym_expr.label("ym"), sa_func.count(MovimientoInventario.id))
        .filter(MovimientoInventario.creado_en.isnot(None))
        .group_by(ym_expr)
        .order_by(ym_expr)
        .all()
    )
    tail = rows[-months:] if len(rows) > months else rows
    labels: list[str] = []
    values: list[int] = []
    for ym, cnt in tail:
        if not ym:
            continue
        parts = str(ym).split("-")
        if len(parts) == 2:
            yy, mm = parts[0], parts[1]
            labels.append(f"{mm}/{yy[-2:]}")
        else:
            labels.append(str(ym))
        values.append(int(cnt))
    return {"labels": labels, "values": values}
