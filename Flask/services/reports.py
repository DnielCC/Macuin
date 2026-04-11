"""Construcción de datos de reporte y generación PDF (personalizable)."""

from __future__ import annotations

import io
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from services.api import MacuinApi, get_api


def available_sections_for_role(rol: str) -> List[Dict[str, str]]:
    """Metadatos de secciones que cada rol puede incluir en el PDF."""
    base = [
        {"id": "portada", "label": "Portada (título, fecha, usuario)"},
        {"id": "resumen", "label": "Resumen ejecutivo (KPIs texto)"},
    ]
    if rol == "Administrador":
        base += [
            {"id": "usuarios", "label": "Tabla de usuarios internos"},
            {"id": "roles", "label": "Roles del sistema"},
            {"id": "autopartes", "label": "Catálogo de autopartes (primeras N filas)"},
            {"id": "pedidos", "label": "Pedidos (primeras N filas)"},
            {"id": "parametros", "label": "Parámetros de sistema"},
        ]
    elif rol == "Ventas":
        base += [
            {"id": "clientes", "label": "Clientes"},
            {"id": "pedidos", "label": "Pedidos"},
            {"id": "autopartes", "label": "Catálogo (consulta)"},
        ]
    elif rol == "Logística":
        base += [
            {"id": "pedidos", "label": "Pedidos y estatus"},
            {"id": "guias", "label": "Guías de envío"},
            {"id": "direcciones", "label": "Direcciones (listado)"},
        ]
    elif rol == "Almacén":
        base += [
            {"id": "inventarios", "label": "Inventario actual"},
            {"id": "ubicaciones", "label": "Ubicaciones"},
            {"id": "pedidos", "label": "Pedidos (surtido/empaque)"},
            {"id": "autopartes", "label": "Autopartes (referencia)"},
        ]
    return base


def _lim_rows(rows: List[List[Any]], max_rows: int) -> List[List[Any]]:
    if len(rows) <= max_rows + 1:
        return rows
    head = rows[: max_rows + 1]
    head.append(["…", f"(Recorte: {len(rows) - 1 - max_rows} filas más)"])
    return head


def build_report_context(
    api: MacuinApi,
    rol: str,
    options: Dict[str, Any],
) -> Dict[str, Any]:
    """options: sections (list str), max_rows (int), title (str), notes (str)"""
    sections: List[Dict[str, Any]] = []
    title = (options.get("title") or f"Reporte Macuin — {rol}").strip()[:200]
    notes = (options.get("notes") or "").strip()[:2000]
    max_rows = int(options.get("max_rows") or 80)
    max_rows = max(5, min(max_rows, 500))
    chosen = set(options.get("sections") or ["portada", "resumen"])

    def add_table(title_p: str, headers: List[str], data_rows: List[List[Any]]):
        grid = [headers] + data_rows
        grid = _lim_rows(grid, max_rows)
        sections.append({"type": "table", "title": title_p, "headers": grid[0], "rows": grid[1:]})

    if "portada" in chosen:
        sections.append(
            {
                "type": "text",
                "title": "Portada",
                "body": f"{title}\nGenerado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\nPerfil: {rol}",
            }
        )
    if "resumen" in chosen:
        sections.append(
            {
                "type": "text",
                "title": "Notas / resumen",
                "body": notes or "Sin notas adicionales.",
            }
        )

    try:
        if "usuarios" in chosen and rol == "Administrador":
            raw = api.get("/v1/usuarios/")
            usuarios = raw.get("usuarios", []) if isinstance(raw, dict) else []
            rows = [
                [u.get("id"), u.get("nombre"), u.get("apellidos"), u.get("email"), u.get("rol_id"), u.get("activo")]
                for u in usuarios
            ]
            add_table("Usuarios", ["ID", "Nombre", "Apellidos", "Email", "Rol ID", "Activo"], rows)

        if "roles" in chosen and rol == "Administrador":
            roles = api.get("/v1/roles/")
            rows = [[r.get("id"), r.get("nombre_rol"), r.get("descripcion")] for r in roles]
            add_table("Roles", ["ID", "Nombre", "Descripción"], rows)

        if "clientes" in chosen and rol in ("Administrador", "Ventas"):
            clientes = api.get("/v1/clientes/")
            rows = [
                [c.get("id"), c.get("nombre"), c.get("email"), c.get("telefono"), c.get("activo")]
                for c in clientes
            ]
            add_table("Clientes", ["ID", "Nombre", "Email", "Teléfono", "Activo"], rows)

        if "autopartes" in chosen:
            partes = api.get("/v1/autopartes/")
            rows = [
                [p.get("id"), p.get("sku_codigo"), p.get("nombre"), p.get("precio_unitario"), p.get("categoria_id"), p.get("marca_id")]
                for p in partes
            ]
            add_table("Autopartes", ["ID", "SKU", "Nombre", "Precio", "Cat", "Marca"], rows)

        if "pedidos" in chosen:
            pedidos = api.get("/v1/pedidos/")
            rows = [
                [
                    p.get("id"),
                    p.get("folio"),
                    p.get("usuario_id"),
                    p.get("cliente_id"),
                    p.get("estatus_id"),
                    str(p.get("total")),
                ]
                for p in pedidos
            ]
            add_table("Pedidos", ["ID", "Folio", "Usuario", "Cliente", "Estatus", "Total"], rows)

        if "parametros" in chosen and rol == "Administrador":
            pars = api.get("/v1/parametros-sistema/")
            rows = [[p.get("id"), p.get("tipo"), p.get("clave"), p.get("valor"), p.get("activo")] for p in pars]
            add_table("Parámetros", ["ID", "Tipo", "Clave", "Valor", "Activo"], rows)

        if "guias" in chosen and rol in ("Administrador", "Logística"):
            guias = api.get("/v1/guias-envio/")
            rows = [
                [g.get("id"), g.get("pedido_id"), g.get("tipo"), g.get("paqueteria"), g.get("numero_rastreo")]
                for g in guias
            ]
            add_table("Guías", ["ID", "Pedido", "Tipo", "Paquetería", "Rastreo"], rows)

        if "direcciones" in chosen and rol in ("Administrador", "Logística"):
            dirs = api.get("/v1/direcciones/")
            rows = [
                [d.get("id"), d.get("calle_principal"), d.get("cp"), d.get("municipio"), d.get("cliente_id")]
                for d in dirs
            ]
            add_table("Direcciones", ["ID", "Calle", "CP", "Municipio", "Cliente ID"], rows)

        if "inventarios" in chosen and rol in ("Administrador", "Almacén"):
            inv = api.get("/v1/inventarios/")
            rows = [
                [i.get("id"), i.get("autoparte_id"), i.get("stock_actual"), i.get("stock_minimo"), i.get("ubicacion_id")]
                for i in inv
            ]
            add_table("Inventarios", ["ID", "Autoparte", "Stock", "Mínimo", "Ubicación"], rows)

        if "ubicaciones" in chosen and rol in ("Administrador", "Almacén"):
            ubi = api.get("/v1/ubicaciones/")
            rows = [[u.get("id"), u.get("pasillo"), u.get("estante"), u.get("capacidad"), u.get("activo")] for u in ubi]
            add_table("Ubicaciones", ["ID", "Pasillo", "Estante", "Capacidad", "Activo"], rows)

    except Exception as exc:
        sections.append({"type": "text", "title": "Error al cargar datos", "body": str(exc)})

    return {"title": title, "rol": rol, "sections": sections, "generated_at": datetime.now(timezone.utc).isoformat()}


def render_pdf(context: Dict[str, Any]) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, title=context.get("title", "Reporte")[:40])
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(context["title"], styles["Title"]))
    story.append(Spacer(1, 12))
    for sec in context.get("sections", []):
        if sec["type"] == "text":
            story.append(Paragraph(sec["title"], styles["Heading2"]))
            story.append(Paragraph(sec.get("body", "").replace("\n", "<br/>"), styles["BodyText"]))
            story.append(Spacer(1, 10))
        elif sec["type"] == "table":
            story.append(Paragraph(sec["title"], styles["Heading2"]))
            data = [sec["headers"]] + sec["rows"]
            t = Table(data, repeatRows=1)
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                    ]
                )
            )
            story.append(t)
            story.append(Spacer(1, 14))
    doc.build(story)
    return buf.getvalue()
