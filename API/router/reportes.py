"""Cuatro tipos de reporte distintos (datos JSON) para cumplimiento de rúbrica y documentación."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from database.autoparte import Autoparte
from database.categoria import Categoria
from database.cliente import Cliente
from database.db import get_db
from database.detalle_pedido import DetallePedido
from database.direccion import Direccion
from database.estatus_pedido import EstatusPedido
from database.inventario import Inventario
from database.marca import Marca
from database.pedido import Pedido
from database.rol import Rol
from database.ubicacion import Ubicacion
from database.usuario import Usuario

router_reportes = APIRouter(prefix="/v1/reportes", tags=["Reportes"])


def _ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@router_reportes.get("/pedidos")
def reporte_pedidos(
    limit: int = Query(300, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Tipo 1: listado operativo de pedidos (enriquecido)."""
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
    filas = []
    for ped, cli, dire, est, piezas in rows:
        dest = "—"
        if dire is not None:
            m, e = (dire.municipio or "").strip(), (dire.estado or "").strip()
            dest = ", ".join(x for x in (m, e) if x) or "—"
        fp = ped.fecha_pedido
        filas.append(
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
            }
        )
    return {
        "tipo_reporte": "pedidos",
        "descripcion": "Pedidos con cliente, destino, piezas y estatus",
        "generado_en": _ahora_iso(),
        "total_registros": len(filas),
        "filas": filas,
    }


@router_reportes.get("/catalogo-autopartes")
def reporte_catalogo_autopartes(
    limit: int = Query(500, ge=1, le=2000),
    db: Session = Depends(get_db),
):
    """Tipo 2: catálogo de autopartes con categoría y marca."""
    rows = (
        db.query(Autoparte, Categoria.nombre, Marca.nombre)
        .join(Categoria, Autoparte.categoria_id == Categoria.id)
        .join(Marca, Autoparte.marca_id == Marca.id)
        .order_by(Autoparte.id)
        .limit(limit)
        .all()
    )
    filas = []
    for ap, cat_nom, mar_nom in rows:
        filas.append(
            {
                "id": ap.id,
                "sku_codigo": ap.sku_codigo,
                "nombre": ap.nombre,
                "precio_unitario": float(ap.precio_unitario or 0),
                "categoria": cat_nom,
                "marca": mar_nom,
            }
        )
    return {
        "tipo_reporte": "catalogo_autopartes",
        "descripcion": "SKU, nombre, precio, categoría y marca",
        "generado_en": _ahora_iso(),
        "total_registros": len(filas),
        "filas": filas,
    }


@router_reportes.get("/usuarios-internos")
def reporte_usuarios_internos(db: Session = Depends(get_db)):
    """Tipo 3: usuarios internos (sin contraseña)."""
    rows = (
        db.query(Usuario, Rol.nombre_rol)
        .join(Rol, Usuario.rol_id == Rol.id)
        .order_by(Usuario.id)
        .all()
    )
    filas = []
    for u, nombre_rol in rows:
        filas.append(
            {
                "id": u.id,
                "nombre": u.nombre,
                "apellidos": u.apellidos,
                "email": u.email,
                "telefono": u.telefono,
                "rol": nombre_rol,
                "activo": u.activo,
            }
        )
    return {
        "tipo_reporte": "usuarios_internos",
        "descripcion": "Personal interno y rol asignado",
        "generado_en": _ahora_iso(),
        "total_registros": len(filas),
        "filas": filas,
    }


@router_reportes.get("/inventario-almacen")
def reporte_inventario_almacen(
    limit: int = Query(500, ge=1, le=2000),
    db: Session = Depends(get_db),
):
    """Tipo 4: inventario con autoparte y ubicación de almacén."""
    rows = (
        db.query(Inventario, Autoparte, Ubicacion)
        .join(Autoparte, Inventario.autoparte_id == Autoparte.id)
        .outerjoin(Ubicacion, Inventario.ubicacion_id == Ubicacion.id)
        .order_by(Inventario.id)
        .limit(limit)
        .all()
    )
    filas = []
    for inv, ap, ubi in rows:
        if ubi is not None:
            ubi_txt = f"{ubi.pasillo}-{ubi.estante}" + (f"-{ubi.nivel}" if ubi.nivel else "")
        else:
            inv_p = (inv.pasillo or "").strip()
            inv_e = (inv.estante or "").strip()
            inv_n = (inv.nivel or "").strip()
            ubi_txt = (
                f"{inv_p}-{inv_e}" + (f"-{inv_n}" if inv_n else "")
                if (inv_p or inv_e)
                else "—"
            )
        filas.append(
            {
                "inventario_id": inv.id,
                "sku_codigo": ap.sku_codigo,
                "autoparte_nombre": ap.nombre,
                "stock_actual": inv.stock_actual,
                "stock_minimo": inv.stock_minimo,
                "ubicacion": ubi_txt,
            }
        )
    return {
        "tipo_reporte": "inventario_almacen",
        "descripcion": "Existencias por autoparte y ubicación",
        "generado_en": _ahora_iso(),
        "total_registros": len(filas),
        "filas": filas,
    }
