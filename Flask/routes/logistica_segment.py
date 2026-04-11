"""Módulo Logística: envíos, direcciones, guías."""

from __future__ import annotations

from flask import flash, redirect, render_template, request, session, url_for

from routes import api_helpers
from services.api import ApiError, get_api
from services.stats import conteo_estatus_pedidos, logistica_kpis, pedidos_por_mes
from services.validators import require_non_empty, validate_float, validate_int, validate_short_text


def register(app):
    def requiere_login():
        return "user_id" not in session

    def solo_logistica():
        if requiere_login():
            return redirect(url_for("login"))
        if session.get("user_role") != "Logística":
            return redirect(url_for("index"))
        return None

    def _estatus_map(api) -> dict:
        try:
            lst = api.get("/v1/estatus-pedido/")
            return {int(e["id"]): e.get("nombre", "") for e in lst}
        except ApiError:
            return {}

    def _enriquecer_pedidos(api, pedidos: list) -> list:
        id_est = _estatus_map(api)
        clientes = {}
        try:
            for c in api.get("/v1/clientes/"):
                clientes[int(c["id"])] = c.get("nombre") or ""
        except ApiError:
            pass
        out = []
        for p in pedidos:
            q = dict(p)
            cid = p.get("cliente_id")
            q["_cliente_nombre"] = clientes.get(int(cid), "—") if cid else "—"
            q["_estatus_nombre"] = id_est.get(int(p.get("estatus_id") or 0), "")
            out.append(q)
        return out

    @app.route("/logistica")
    @app.route("/logistica/dashboard")
    def logistica_dashboard():
        redir = solo_logistica()
        if redir:
            return redir
        api = get_api()
        try:
            pedidos = api.get("/v1/pedidos/")
            estatus = api.get("/v1/estatus-pedido/")
            guias = api.get("/v1/guias-envio/")
            kpis = logistica_kpis(pedidos, estatus)
            lbl_m, dat_m = pedidos_por_mes(pedidos)
            lbl_e, dat_e = conteo_estatus_pedidos(pedidos, estatus)
            guias_total = len(guias)
        except ApiError as e:
            flash(str(e.message), "danger")
            kpis = {}
            lbl_m, dat_m, lbl_e, dat_e = [], [], [], []
            guias = []
            guias_total = 0
        return render_template(
            "logistica_dashboard.html",
            kpi=kpis,
            chart_mes_labels=lbl_m,
            chart_mes_data=dat_m,
            chart_estatus_labels=lbl_e,
            chart_estatus_data=dat_e,
            guias_recientes=guias[:6],
            guias_total=guias_total,
        )

    @app.route("/logistica/envios", methods=["GET"])
    def logistica_envios():
        redir = solo_logistica()
        if redir:
            return redir
        api = get_api()
        try:
            pedidos = api.get("/v1/pedidos/")
            pedidos_e = _enriquecer_pedidos(api, pedidos)
        except ApiError as e:
            flash(str(e.message), "danger")
            pedidos_e = []
        return render_template("logistica_envios.html", pedidos=pedidos_e)

    @app.route("/logistica/envios/<int:pedido_id>/estatus", methods=["POST"])
    def logistica_envios_estatus(pedido_id):
        redir = solo_logistica()
        if redir:
            return redir
        nombre = (request.form.get("estatus") or "").strip()
        if nombre not in ("Enviado", "Entregado"):
            flash("Estatus no permitido.", "danger")
            return redirect(url_for("logistica_envios"))
        api = get_api()
        eid = api_helpers.estatus_por_nombre(api, nombre)
        if not eid:
            flash("Estatus no encontrado en catálogo.", "danger")
            return redirect(url_for("logistica_envios"))
        try:
            api.patch(f"/v1/pedidos/{pedido_id}/estatus", json={"estatus_id": eid})
            flash(f"Pedido actualizado a «{nombre}».", "success")
        except ApiError as e:
            flash(str(e.message), "danger")
        return redirect(url_for("logistica_envios"))

    @app.route("/logistica/direcciones")
    def logistica_direcciones():
        redir = solo_logistica()
        if redir:
            return redir
        api = get_api()
        try:
            direcciones = api.get("/v1/direcciones/")
            clientes = {c["id"]: c.get("nombre") for c in api.get("/v1/clientes/")}
            for d in direcciones:
                cid = d.get("cliente_id")
                d["_cliente_nombre"] = clientes.get(cid, "—") if cid else "Interno / sin cliente"
        except ApiError as e:
            flash(str(e.message), "danger")
            direcciones = []
        return render_template("logistica_direcciones.html", direcciones=direcciones)

    @app.route("/logistica/guias", methods=["GET", "POST"])
    def logistica_guias():
        redir = solo_logistica()
        if redir:
            return redir
        api = get_api()
        if request.method == "POST":
            act = request.form.get("_action")
            if act == "nueva":
                ok, err, pid = validate_int(request.form.get("pedido_id"), "Pedido")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("logistica_guias"))
                ok, tipo = validate_short_text(request.form.get("tipo"), "Tipo", 40)
                if not ok:
                    flash(tipo, "danger")
                    return redirect(url_for("logistica_guias"))
                ok, paq = validate_short_text(request.form.get("paqueteria"), "Paquetería", 80)
                if not ok:
                    flash(paq, "danger")
                    return redirect(url_for("logistica_guias"))
                rastreo = (request.form.get("numero_rastreo") or "").strip()[:120] or None
                ok_w, err_w, peso = validate_float(request.form.get("peso_kg"), "Peso (kg)", min_v=0.0)
                peso_val = float(peso) if ok_w and peso is not None else None
                if request.form.get("peso_kg") and not ok_w:
                    flash(err_w, "danger")
                    return redirect(url_for("logistica_guias"))
                servicio = (request.form.get("servicio") or "").strip()[:80] or None
                notas = (request.form.get("notas_entrega") or "").strip()[:500] or None
                try:
                    api.post(
                        "/v1/guias-envio/",
                        json={
                            "pedido_id": pid,
                            "tipo": tipo,
                            "paqueteria": paq,
                            "numero_rastreo": rastreo,
                            "peso_kg": peso_val,
                            "servicio": servicio,
                            "notas_entrega": notas,
                            "archivo_url": None,
                        },
                    )
                    flash("Guía registrada.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "editar":
                ok, err, gid = validate_int(request.form.get("guia_id"), "ID guía")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("logistica_guias"))
                body = {}
                if request.form.get("paqueteria"):
                    body["paqueteria"] = request.form.get("paqueteria", "").strip()[:80]
                if request.form.get("numero_rastreo") is not None:
                    body["numero_rastreo"] = (request.form.get("numero_rastreo") or "").strip()[:120] or None
                if request.form.get("tipo"):
                    body["tipo"] = request.form.get("tipo", "").strip()[:40]
                if not body:
                    flash("No hay cambios que guardar.", "warning")
                    return redirect(url_for("logistica_guias"))
                try:
                    api.put(f"/v1/guias-envio/{gid}", json=body)
                    flash("Guía actualizada.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "eliminar":
                ok, err, gid = validate_int(request.form.get("guia_id"), "ID guía")
                if ok:
                    try:
                        api.delete(f"/v1/guias-envio/{gid}")
                        flash("Guía eliminada.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(err, "danger")
            return redirect(url_for("logistica_guias"))

        try:
            guias = api.get("/v1/guias-envio/")
            pedidos = api.get("/v1/pedidos/")
        except ApiError as e:
            flash(str(e.message), "danger")
            guias, pedidos = [], []
        return render_template("logistica_guias.html", guias=guias, pedidos=pedidos)
