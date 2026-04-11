"""Mapeos nombre ↔ id contra la API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from services.api import MacuinApi


def estatus_por_nombre(api: MacuinApi, nombre: str) -> Optional[int]:
    lst = api.get("/v1/estatus-pedido/")
    for e in lst:
        if (e.get("nombre") or "").strip().lower() == (nombre or "").strip().lower():
            return int(e["id"])
    return None


def rol_por_nombre(api: MacuinApi, nombre: str) -> Optional[int]:
    for r in api.get("/v1/roles/"):
        if (r.get("nombre_rol") or "").strip().lower() == (nombre or "").strip().lower():
            return int(r["id"])
    return None


def categoria_por_nombre(api: MacuinApi, nombre: str) -> Optional[int]:
    for c in api.get("/v1/categorias/"):
        if (c.get("nombre") or "").strip().lower() == (nombre or "").strip().lower():
            return int(c["id"])
    return None


def marca_por_nombre(api: MacuinApi, nombre: str) -> Optional[int]:
    for m in api.get("/v1/marcas/"):
        if (m.get("nombre") or "").strip().lower() == (nombre or "").strip().lower():
            return int(m["id"])
    return None


def autoparte_por_sku(api: MacuinApi, sku: str) -> Optional[Dict[str, Any]]:
    sku = (sku or "").strip()
    if not sku:
        return None
    for p in api.get("/v1/autopartes/"):
        if (p.get("sku_codigo") or "").strip().upper() == sku.upper():
            return p
    return None
