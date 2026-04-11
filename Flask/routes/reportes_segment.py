"""Reportes PDF personalizables: configuración, vista previa y descarga."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import flash, make_response, redirect, render_template, request, session, url_for

from services.api import ApiError, get_api
from services.reports import available_sections_for_role, build_report_context, render_pdf
from services.validators import validate_int


def register(app):
    def requiere_login():
        return "user_id" not in session

    def solo_logueado():
        if requiere_login():
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
        return {
            "title": title or None,
            "notes": notes or None,
            "sections": list(sections),
            "max_rows": max_rows,
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

    @app.route("/reportes/pdf", methods=["POST"])
    def reportes_pdf():
        redir = solo_logueado()
        if redir:
            return redir
        rol = session.get("user_role") or "General"
        api = get_api()
        try:
            opts = _parse_options_from_form()
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("reportes_index"))
        try:
            ctx = build_report_context(api, rol, opts)
            pdf_bytes = render_pdf(ctx)
        except ApiError as e:
            flash(str(e.message), "danger")
            return redirect(url_for("reportes_index"))
        fname = f"macuin_reporte_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.pdf"
        resp = make_response(pdf_bytes)
        resp.headers["Content-Type"] = "application/pdf"
        resp.headers["Content-Disposition"] = f'attachment; filename="{fname}"'
        return resp
