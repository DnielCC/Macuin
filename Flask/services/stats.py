"""Agregados para dashboards (gráficas reales a partir de la API)."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def _as_list(data: Any) -> List[dict]:
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "usuarios" in data:
            return list(data["usuarios"])
        if "pedidos" in data:
            return list(data["pedidos"])
    return []


def _parse_dt(val: Any) -> Optional[datetime]:
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    s = str(val).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def pedidos_por_mes(pedidos: List[dict], last_n_months: int = 6) -> Tuple[List[str], List[int]]:
    buckets: Dict[str, int] = defaultdict(int)
    for p in pedidos:
        dt = _parse_dt(p.get("fecha_pedido"))
        if not dt:
            continue
        key = dt.strftime("%Y-%m")
        buckets[key] += 1
    keys_sorted = sorted(buckets.keys())[-last_n_months:]
    labels = []
    values = []
    for k in keys_sorted:
        yy, mm = k.split("-")
        labels.append(f"{mm}/{yy[-2:]}")
        values.append(buckets[k])
    return labels, values


def conteo_roles(usuarios: List[dict], roles: List[dict]) -> Tuple[List[str], List[int]]:
    id_to_name = {r["id"]: r.get("nombre_rol", "?") for r in roles}
    counts: Dict[str, int] = defaultdict(int)
    for u in usuarios:
        rid = u.get("rol_id")
        counts[id_to_name.get(rid, "Sin rol")] += 1
    labels = list(counts.keys())
    vals = [counts[k] for k in labels]
    return labels, vals


def ventas_kpis(pedidos: List[dict], clientes: List[dict]) -> Dict[str, Any]:
    activos = sum(1 for c in clientes if c.get("activo", True))
    total_pedidos = len(pedidos)
    cancelados = sum(1 for p in pedidos if p.get("motivo_cancelacion"))
    return {
        "total_pedidos": total_pedidos,
        "clientes_activos": activos,
        "pedidos_cancelados": cancelados,
    }


def logistica_kpis(pedidos: List[dict], estatus: List[dict]) -> Dict[str, Any]:
    id_to = {e["id"]: e.get("nombre", "") for e in estatus}
    enviados = sum(1 for p in pedidos if id_to.get(p.get("estatus_id")) == "Enviado")
    entregados = sum(1 for p in pedidos if id_to.get(p.get("estatus_id")) == "Entregado")
    cancelados = sum(1 for p in pedidos if id_to.get(p.get("estatus_id")) == "Cancelado")
    return {
        "enviados": enviados,
        "entregados": entregados,
        "cancelados": cancelados,
        "total_pedidos": len(pedidos),
    }


def almacen_kpis(inventarios: List[dict], pedidos: List[dict], estatus: List[dict]) -> Dict[str, Any]:
    id_to = {e["id"]: e.get("nombre", "") for e in estatus}
    surtiendo = sum(1 for p in pedidos if id_to.get(p.get("estatus_id")) == "Surtiendo")
    empacado = sum(1 for p in pedidos if id_to.get(p.get("estatus_id")) == "Empacado")
    stock_bajo = sum(
        1
        for inv in inventarios
        if int(inv.get("stock_actual") or 0) <= int(inv.get("stock_minimo") or 0)
    )
    return {"surtiendo": surtiendo, "empacado": empacado, "alertas_stock": stock_bajo}


def admin_kpis(usuarios: List[dict], autopartes: List[dict], pedidos: List[dict], parametros: List[dict]) -> Dict[str, Any]:
    activos = sum(1 for u in usuarios if u.get("activo", True))
    return {
        "usuarios_activos": activos,
        "usuarios_total": len(usuarios),
        "skus": len(autopartes),
        "pedidos": len(pedidos),
        "parametros": len(parametros),
    }


def _total_pedido_num(p: dict) -> float:
    try:
        return float(p.get("total") or 0)
    except (TypeError, ValueError):
        return 0.0


def totales_pedidos_por_mes(pedidos: List[dict], last_n_months: int = 6) -> Tuple[List[str], List[float]]:
    """Suma de campo total por mes (para gráfica de ingresos aproximados)."""
    buckets: Dict[str, float] = defaultdict(float)
    for p in pedidos:
        dt = _parse_dt(p.get("fecha_pedido"))
        if not dt:
            continue
        key = dt.strftime("%Y-%m")
        buckets[key] += _total_pedido_num(p)
    keys_sorted = sorted(buckets.keys())[-last_n_months:]
    labels = []
    values = []
    for k in keys_sorted:
        yy, mm = k.split("-")
        labels.append(f"{mm}/{yy[-2:]}")
        values.append(round(buckets[k], 2))
    return labels, values


def conteo_estatus_pedidos(pedidos: List[dict], estatus: List[dict]) -> Tuple[List[str], List[int]]:
    id_to = {e["id"]: e.get("nombre", "?") for e in estatus}
    counts: Dict[str, int] = defaultdict(int)
    for p in pedidos:
        counts[id_to.get(p.get("estatus_id"), "Sin estatus")] += 1
    labels = list(counts.keys())
    vals = [counts[k] for k in labels]
    return labels, vals
