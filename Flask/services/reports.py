"""Construcción de datos de reporte y generación PDF (personalizable, UTF-8, tablas legibles)."""

from __future__ import annotations

import io
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from xml.sax.saxutils import escape

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from services.api import MacuinApi

_FONT_BODY = "Helvetica"
_FONT_TITLE = "Helvetica-Bold"


def _register_unicode_font() -> Tuple[str, str]:
    """Registra DejaVu Sans si existe en el paquete reportlab (acentos y ñ en PDF)."""
    global _FONT_BODY, _FONT_TITLE
    try:
        pkg = os.path.dirname(reportlab.__file__)
        regular = os.path.join(pkg, "fonts", "DejaVuSans.ttf")
        bold = os.path.join(pkg, "fonts", "DejaVuSans-Bold.ttf")
        if os.path.isfile(regular):
            pdfmetrics.registerFont(TTFont("DejaVuSans", regular))
            _FONT_BODY = "DejaVuSans"
            if os.path.isfile(bold):
                pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", bold))
                _FONT_TITLE = "DejaVuSans-Bold"
            else:
                _FONT_TITLE = "DejaVuSans"
    except Exception:
        pass
    return _FONT_BODY, _FONT_TITLE


_register_unicode_font()


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
            {"id": "mensajes_contacto", "label": "Mensajes de contacto del portal web"},
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
    """Limita filas de datos (sin cabecera)."""
    if len(rows) <= max_rows:
        return rows
    head = rows[:max_rows]
    n_extra = len(rows) - max_rows
    nc = len(rows[0]) if rows else 1
    note = [f"… ({n_extra} filas adicionales no mostradas)"] + [""] * (nc - 1)
    head.append(note[:nc])
    return head


def _safe(s: Any) -> str:
    if s is None:
        return "—"
    return str(s)


def _lookup_maps(api: MacuinApi) -> Dict[str, Dict[int, str]]:
    """Mapas id → texto legible para sustituir FKs en tablas."""
    maps: Dict[str, Dict[int, str]] = {
        "rol": {},
        "categoria": {},
        "marca": {},
        "estatus": {},
        "cliente": {},
        "ubicacion": {},
        "autoparte": {},
        "pedido_folio": {},
    }
    try:
        for r in api.get("/v1/roles/") or []:
            rid = r.get("id") if isinstance(r, dict) else getattr(r, "id", None)
            if rid is not None:
                nom = (r.get("nombre_rol") if isinstance(r, dict) else getattr(r, "nombre_rol", "")) or ""
                maps["rol"][int(rid)] = nom
    except Exception:
        pass
    try:
        for c in api.get("/v1/categorias/") or []:
            cid = c.get("id") if isinstance(c, dict) else getattr(c, "id", None)
            if cid is not None:
                maps["categoria"][int(cid)] = (c.get("nombre") if isinstance(c, dict) else getattr(c, "nombre", "")) or ""
    except Exception:
        pass
    try:
        for m in api.get("/v1/marcas/") or []:
            mid = m.get("id") if isinstance(m, dict) else getattr(m, "id", None)
            if mid is not None:
                maps["marca"][int(mid)] = (m.get("nombre") if isinstance(m, dict) else getattr(m, "nombre", "")) or ""
    except Exception:
        pass
    try:
        for e in api.get("/v1/estatus-pedido/") or []:
            eid = e.get("id") if isinstance(e, dict) else getattr(e, "id", None)
            if eid is not None:
                maps["estatus"][int(eid)] = (e.get("nombre") if isinstance(e, dict) else getattr(e, "nombre", "")) or ""
    except Exception:
        pass
    try:
        for c in api.get("/v1/clientes/") or []:
            cid = c.get("id") if isinstance(c, dict) else getattr(c, "id", None)
            if cid is not None:
                maps["cliente"][int(cid)] = (c.get("nombre") if isinstance(c, dict) else getattr(c, "nombre", "")) or ""
    except Exception:
        pass
    try:
        for u in api.get("/v1/ubicaciones/") or []:
            uid = u.get("id") if isinstance(u, dict) else getattr(u, "id", None)
            if uid is not None:
                p, es, nv = (
                    (u.get("pasillo"), u.get("estante"), u.get("nivel"))
                    if isinstance(u, dict)
                    else (getattr(u, "pasillo", ""), getattr(u, "estante", ""), getattr(u, "nivel", None))
                )
                lbl = f"{p}-{es}" + (f"-{nv}" if nv else "")
                maps["ubicacion"][int(uid)] = lbl
    except Exception:
        pass
    try:
        for a in api.get("/v1/autopartes/") or []:
            aid = a.get("id") if isinstance(a, dict) else getattr(a, "id", None)
            if aid is not None:
                sku = (a.get("sku_codigo") if isinstance(a, dict) else getattr(a, "sku_codigo", "")) or ""
                nom = (a.get("nombre") if isinstance(a, dict) else getattr(a, "nombre", "")) or ""
                maps["autoparte"][int(aid)] = f"{sku} — {nom[:50]}"
    except Exception:
        pass
    try:
        vista = api.get("/v1/pedidos/admin/vista", params={"limit": 500}) or []
        for p in vista:
            if isinstance(p, dict) and p.get("id") is not None:
                maps["pedido_folio"][int(p["id"])] = _safe(p.get("folio"))
    except Exception:
        pass
    return maps


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
    maps = _lookup_maps(api)

    def add_table(title_p: str, headers: List[str], data_rows: List[List[Any]]):
        data_rows = _lim_rows(data_rows, max_rows)
        sections.append({"type": "table", "title": title_p, "headers": headers, "rows": data_rows})

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
            rows = []
            for u in usuarios:
                if not isinstance(u, dict):
                    u = {k: getattr(u, k, None) for k in ("id", "nombre", "apellidos", "email", "rol_id", "activo")}
                rid = u.get("rol_id")
                rol_txt = maps["rol"].get(int(rid), "—") if rid is not None else "—"
                rows.append(
                    [
                        _safe(u.get("nombre")),
                        _safe(u.get("apellidos")),
                        _safe(u.get("email")),
                        rol_txt,
                        "Sí" if u.get("activo") else "No",
                    ]
                )
            add_table("Usuarios internos", ["Nombre", "Apellidos", "Correo", "Rol", "Activo"], rows)

        if "roles" in chosen and rol == "Administrador":
            roles = api.get("/v1/roles/") or []
            rows = []
            for r in roles:
                if not isinstance(r, dict):
                    r = {k: getattr(r, k, None) for k in ("nombre_rol", "descripcion")}
                rows.append([_safe(r.get("nombre_rol")), _safe(r.get("descripcion"))])
            add_table("Roles del sistema", ["Rol", "Descripción"], rows)

        if "clientes" in chosen and rol in ("Administrador", "Ventas"):
            clientes = api.get("/v1/clientes/") or []
            rows = []
            for c in clientes:
                if not isinstance(c, dict):
                    c = {k: getattr(c, k, None) for k in ("nombre", "email", "telefono", "activo", "notas")}
                rows.append(
                    [
                        _safe(c.get("nombre")),
                        _safe(c.get("email")),
                        _safe(c.get("telefono")),
                        "Sí" if c.get("activo") else "No",
                        (_safe(c.get("notas"))[:80] + "…") if c.get("notas") and len(_safe(c.get("notas"))) > 80 else _safe(c.get("notas")),
                    ]
                )
            add_table("Clientes", ["Nombre", "Correo", "Teléfono", "Activo", "Notas (extracto)"], rows)

        if "autopartes" in chosen:
            partes = api.get("/v1/autopartes/") or []
            rows = []
            for p in partes:
                if not isinstance(p, dict):
                    p = {k: getattr(p, k, None) for k in ("sku_codigo", "nombre", "precio_unitario", "categoria_id", "marca_id")}
                cid, mid = p.get("categoria_id"), p.get("marca_id")
                cat = maps["categoria"].get(int(cid), "—") if cid is not None else "—"
                mar = maps["marca"].get(int(mid), "—") if mid is not None else "—"
                rows.append(
                    [
                        _safe(p.get("sku_codigo")),
                        _safe(p.get("nombre")),
                        _safe(p.get("precio_unitario")),
                        cat,
                        mar,
                    ]
                )
            add_table("Catálogo de autopartes", ["SKU", "Nombre", "Precio unit. (MXN)", "Categoría", "Marca"], rows)

        if "pedidos" in chosen:
            vista = api.get("/v1/pedidos/admin/vista", params={"limit": 500}) or []
            rows = []
            for p in vista:
                if not isinstance(p, dict):
                    continue
                rows.append(
                    [
                        _safe(p.get("folio")),
                        _safe(p.get("cliente_nombre")),
                        _safe(p.get("destino")),
                        _safe(p.get("piezas")),
                        _safe(p.get("estatus")),
                        _safe(p.get("estatus_modulo")),
                        _safe(p.get("total")),
                        (_safe(p.get("fecha_pedido"))[:19] if p.get("fecha_pedido") else "—"),
                    ]
                )
            add_table(
                "Pedidos",
                ["Folio", "Cliente", "Destino (municipio/estado)", "Piezas", "Estatus", "Módulo", "Total MXN", "Fecha"],
                rows,
            )

        if "parametros" in chosen and rol == "Administrador":
            pars = api.get("/v1/parametros-sistema/") or []
            rows = [[_safe(p.get("tipo")), _safe(p.get("clave")), _safe(p.get("valor")), "Sí" if p.get("activo") else "No"] for p in pars]
            add_table("Parámetros de sistema", ["Tipo", "Clave", "Valor", "Activo"], rows)

        if "mensajes_contacto" in chosen and rol == "Administrador":
            msgs = api.get("/v1/portal-contacto/mensajes") or []
            rows = []
            for m in msgs:
                if not isinstance(m, dict):
                    continue
                ar = (m.get("admin_reply") or "").strip()
                reply_snip = (ar[:200] + "…") if len(ar) > 200 else (ar or "—")
                msg_txt = _safe(m.get("mensaje"))
                msg_snip = (msg_txt[:120] + "…") if len(msg_txt) > 120 else msg_txt
                estado = "Contestado" if ar else ("Leído" if m.get("is_read") else "No leído")
                rows.append(
                    [
                        _safe(m.get("id")),
                        (_safe(m.get("creado_en"))[:19] if m.get("creado_en") else "—"),
                        _safe(m.get("nombre")),
                        _safe(m.get("email")),
                        _safe(m.get("asunto")),
                        estado,
                        msg_snip,
                        reply_snip,
                    ]
                )
            add_table(
                "Mensajes de contacto (portal web)",
                ["ID", "Fecha", "Nombre", "Correo", "Asunto", "Estado", "Mensaje (extracto)", "Respuesta admin (extracto)"],
                rows,
            )

        if "guias" in chosen and rol in ("Administrador", "Logística"):
            guias = api.get("/v1/guias-envio/") or []
            rows = []
            for g in guias:
                if not isinstance(g, dict):
                    g = {k: getattr(g, k, None) for k in ("pedido_id", "tipo", "paqueteria", "numero_rastreo")}
                pid = g.get("pedido_id")
                folio = maps["pedido_folio"].get(int(pid), f"Pedido #{pid}") if pid is not None else "—"
                rows.append([folio, _safe(g.get("tipo")), _safe(g.get("paqueteria")), _safe(g.get("numero_rastreo"))])
            add_table("Guías de envío", ["Pedido (folio)", "Tipo", "Paquetería", "Número de rastreo"], rows)

        if "direcciones" in chosen and rol in ("Administrador", "Logística"):
            dirs = api.get("/v1/direcciones/") or []
            rows = []
            for d in dirs:
                if not isinstance(d, dict):
                    d = {
                        k: getattr(d, k, None)
                        for k in ("calle_principal", "num_ext", "colonia", "municipio", "estado", "cp", "cliente_id")
                    }
                cid = d.get("cliente_id")
                cli = maps["cliente"].get(int(cid), "—") if cid is not None else "—"
                rows.append(
                    [
                        cli,
                        _safe(d.get("calle_principal")),
                        _safe(d.get("num_ext")),
                        _safe(d.get("colonia")),
                        _safe(d.get("municipio")),
                        _safe(d.get("estado")),
                        _safe(d.get("cp")),
                    ]
                )
            add_table("Direcciones", ["Cliente", "Calle", "Núm. ext.", "Colonia", "Municipio", "Estado", "C.P."], rows)

        if "inventarios" in chosen and rol in ("Administrador", "Almacén"):
            inv = api.get("/v1/inventarios/") or []
            rows = []
            for i in inv:
                if not isinstance(i, dict):
                    i = {k: getattr(i, k, None) for k in ("autoparte_id", "stock_actual", "stock_minimo", "ubicacion_id")}
                aid, uid = i.get("autoparte_id"), i.get("ubicacion_id")
                ap_lbl = maps["autoparte"].get(int(aid), f"Autoparte #{aid}") if aid is not None else "—"
                ubi = maps["ubicacion"].get(int(uid), "—") if uid is not None else "Sin ubicación"
                rows.append([ap_lbl, _safe(i.get("stock_actual")), _safe(i.get("stock_minimo")), ubi])
            add_table("Inventarios", ["Autoparte", "Stock actual", "Stock mínimo", "Ubicación (pasillo-estante)"], rows)

        if "ubicaciones" in chosen and rol in ("Administrador", "Almacén"):
            ubi = api.get("/v1/ubicaciones/") or []
            rows = []
            for u in ubi:
                if not isinstance(u, dict):
                    u = {k: getattr(u, k, None) for k in ("pasillo", "estante", "nivel", "capacidad", "descripcion", "activo")}
                rows.append(
                    [
                        _safe(u.get("pasillo")),
                        _safe(u.get("estante")),
                        _safe(u.get("nivel")),
                        _safe(u.get("capacidad")),
                        (_safe(u.get("descripcion"))[:60] + "…")
                        if u.get("descripcion") and len(_safe(u.get("descripcion"))) > 60
                        else _safe(u.get("descripcion")),
                        "Sí" if u.get("activo") else "No",
                    ]
                )
            add_table("Ubicaciones de almacén", ["Pasillo", "Estante", "Nivel", "Capacidad", "Descripción", "Activo"], rows)

    except Exception as exc:
        sections.append({"type": "text", "title": "Error al cargar datos", "body": str(exc)})

    return {"title": title, "rol": rol, "sections": sections, "generated_at": datetime.now(timezone.utc).isoformat()}


def render_pdf(context: Dict[str, Any]) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        title=context.get("title", "Reporte")[:60],
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="RepTitle",
        parent=styles["Title"],
        fontName=_FONT_TITLE,
        fontSize=18,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6,
    )
    h2_style = ParagraphStyle(
        name="RepH2",
        parent=styles["Heading2"],
        fontName=_FONT_TITLE,
        fontSize=12,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        name="RepBody",
        parent=styles["BodyText"],
        fontName=_FONT_BODY,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155"),
    )

    story: List[Any] = []
    # Franja de cabecera
    brand = Table([[Paragraph(escape(context.get("title", "Reporte")), title_style)]], colWidths=[17 * cm])
    brand.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbbf24")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#ca8a04")),
            ]
        )
    )
    story.append(brand)
    story.append(Spacer(1, 8))

    for sec in context.get("sections", []):
        if sec["type"] == "text":
            story.append(Paragraph(escape(sec["title"]), h2_style))
            story.append(Paragraph(escape(sec.get("body", "")).replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 8))
        elif sec["type"] == "table":
            story.append(Paragraph(escape(sec["title"]), h2_style))
            hdr = [Paragraph(f"<b>{escape(str(h))}</b>", body_style) for h in sec["headers"]]
            body_rows: List[List[Any]] = [hdr]
            for row in sec["rows"]:
                body_rows.append([Paragraph(escape(_safe(c)), body_style) for c in row])
            t = Table(body_rows, repeatRows=1, hAlign="LEFT")
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("FONTNAME", (0, 0), (-1, 0), _FONT_TITLE),
                        ("FONTSIZE", (0, 0), (-1, 0), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        ("TOPPADDING", (0, 0), (-1, 0), 8),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 1), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
                        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
                        ("LINEBELOW", (0, 0), (-1, 0), 1.2, colors.HexColor("#0f172a")),
                    ]
                )
            )
            story.append(t)
            story.append(Spacer(1, 14))

    doc.build(story)
    return buf.getvalue()
