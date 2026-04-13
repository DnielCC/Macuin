"""Reportes personalizables: vista previa y descarga PDF / Word / Excel."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import flash, make_response, redirect, render_template, request, session, url_for

from services.api import ApiError, get_api
from services.reports import (
    available_sections_for_role,
    build_report_context,
    render_docx,
    render_pdf,
    render_xlsx,
)
from services.validators import validate_int


def register(app):
    def solo_logueado():
        if "user_id" not in session:
            return redirect(url_for("login"))
        return None

    def _parse_options_from_form() -> dict:
        title = (request.form.get("title") or "").strip()
        notes = (request.form.get("notes") or "").strip()
        sections = request.form.getlist("sections")
        if not sections:
            sections = ["portada", "resumen"]
        ok, err, max_rows = validate_int(
            request.form.get("max_rows") or "80", "Máximo de filas", min_v=5, max_v=500
        )
        if not ok:
            raise ValueError(err)
        include_charts = request.form.get("include_charts") == "on"
        return {
            "title": title or None,
            "notes": notes or None,
            "sections": list(sections),
            "max_rows": max_rows,
            "include_charts": include_charts,
        }

    @app.route("/reportes", methods=["GET", "POST"])
    def reportes_index():
        redir = solo_logueado()
        if redir:
            return redir
        rol = session.get("user_role") or "General"
        secciones = available_sections_for_role(rol)
        preview_ctx = None
        api = get_api()
        if request.method == "POST" and request.form.get("_action") == "preview":
            try:
                opts = _parse_options_from_form()
                preview_ctx = build_report_context(api, rol, opts)
            except ValueError as e:
                flash(str(e), "danger")
            except ApiError as e:
                flash(str(e.message), "danger")
        return render_template(
            "reportes_index.html",
            rol=rol,
            secciones_disponibles=secciones,
            preview_ctx=preview_ctx,
        )

    @app.route("/reportes/descargar", methods=["POST"])
    def reportes_descargar():
        redir = solo_logueado()
        if redir:
            return redir
        rol = session.get("user_role") or "General"
        fmt = (request.form.get("fmt") or "").lower().strip()
        if fmt not in ("pdf", "docx", "xlsx"):
            flash("Formato de archivo no válido.", "danger")
            return redirect(url_for("reportes_index"))
        try:
            opts = _parse_options_from_form()
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("reportes_index"))
        api = get_api()
        try:
            ctx = build_report_context(api, rol, opts)
        except ApiError as e:
            flash(str(e.message), "danger")
            return redirect(url_for("reportes_index"))

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
        base = f"macuin_reporte_{ts}"
        try:
            if fmt == "pdf":
                data = render_pdf(ctx)
                resp = make_response(data)
                resp.headers["Content-Type"] = "application/pdf"
                resp.headers["Content-Disposition"] = f'attachment; filename="{base}.pdf"'
                return resp
            if fmt == "docx":
                data = render_docx(ctx)
                resp = make_response(data)
                resp.headers["Content-Type"] = (
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                resp.headers["Content-Disposition"] = f'attachment; filename="{base}.docx"'
                return resp
            data = render_xlsx(ctx)
            resp = make_response(data)
            resp.headers["Content-Type"] = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            resp.headers["Content-Disposition"] = f'attachment; filename="{base}.xlsx"'
            return resp
        except Exception as exc:
            flash(f"No se pudo generar el archivo: {exc}", "danger")
            return redirect(url_for("reportes_index"))
