"""Módulo Almacén: inventario, ubicaciones, pedidos y consulta de autopartes."""

from __future__ import annotations

from flask import flash, redirect, render_template, request, session, url_for

from routes import api_helpers
from services.api import ApiError, get_api
from services.stats import almacen_kpis, conteo_estatus_pedidos
from services.validators import validate_int, validate_short_text


def register(app):
    def requiere_login():
        return "user_id" not in session

    def solo_almacen():
        if requiere_login():
            return redirect(url_for("login"))
        if session.get("user_role") != "Almacén":
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

    @app.route("/almacen")
    @app.route("/almacen/dashboard")
    def almacen_dashboard():
        redir = solo_almacen()
        if redir:
            return redir
        api = get_api()
        try:
            pedidos = api.get("/v1/pedidos/")
            estatus = api.get("/v1/estatus-pedido/")
            inventarios = api.get("/v1/inventarios/")
            ubicaciones = api.get("/v1/ubicaciones/")
            kpis = almacen_kpis(inventarios, pedidos, estatus)
            mov_res = api.get("/v1/movimientos-inventario/resumen-por-mes", params={"months": 6})
            lbl_m = mov_res.get("labels") or []
            dat_m = mov_res.get("values") or []
            lbl_e, dat_e = conteo_estatus_pedidos(pedidos, estatus)
            skus_stock = len(inventarios)
            ubi_activas = sum(1 for u in ubicaciones if u.get("activo", True))
            actividades = api.get("/v1/movimientos-inventario/recientes", params={"limit": 15})
            if not isinstance(actividades, list):
                actividades = []
        except ApiError as e:
            flash(str(e.message), "danger")
            kpis = {}
            lbl_m, dat_m, lbl_e, dat_e = [], [], [], []
            skus_stock = ubi_activas = 0
            actividades = []
        return render_template(
            "almacen_dashboard.html",
            kpi=kpis,
            chart_mes_labels=lbl_m,
            chart_mes_data=dat_m,
            chart_estatus_labels=lbl_e,
            chart_estatus_data=dat_e,
            skus_stock=skus_stock,
            ubicaciones_activas=ubi_activas,
            actividades_recientes=actividades,
        )

    @app.route("/almacen/inventario", methods=["GET"])
    def almacen_inventario():
        redir = solo_almacen()
        if redir:
            return redir
        api = get_api()
        try:
            inventarios = api.get("/v1/inventarios/")
            autopartes = {a["id"]: a for a in api.get("/v1/autopartes/")}
            ubicaciones = {u["id"]: u for u in api.get("/v1/ubicaciones/")}
            for inv in inventarios:
                ap = autopartes.get(inv.get("autoparte_id"), {})
                inv["_sku"] = ap.get("sku_codigo", "")
                inv["_nombre_parte"] = ap.get("nombre", "")
                ub = ubicaciones.get(inv.get("ubicacion_id"), {})
                inv["_ubic_label"] = f"{ub.get('pasillo','')} / {ub.get('estante','')}" if ub else "—"
                inv["_alerta"] = int(inv.get("stock_actual") or 0) <= int(inv.get("stock_minimo") or 0)
        except ApiError as e:
            flash(str(e.message), "danger")
            inventarios = []
        return render_template("almacen_inventario.html", inventarios=inventarios)

    @app.route("/almacen/inventario/ajustar", methods=["POST"])
    def almacen_inventario_ajustar():
        redir = solo_almacen()
        if redir:
            return redir
        api = get_api()
        ok, err, iid = validate_int(request.form.get("inventario_id"), "Inventario")
        if not ok:
            flash(err, "danger")
            return redirect(url_for("almacen_inventario"))
        tipo = (request.form.get("tipo") or "").strip().lower()
        if tipo not in ("entrada", "merma"):
            flash("Tipo de movimiento no válido.", "danger")
            return redirect(url_for("almacen_inventario"))
        ok, err2, cant = validate_int(request.form.get("cantidad"), "Cantidad", min_v=1, max_v=100000)
        if not ok:
            flash(err2, "danger")
            return redirect(url_for("almacen_inventario"))
        notas = (request.form.get("notas") or "").strip()[:500] or None
        uid = session.get("user_id")
        try:
            api.post(
                f"/v1/inventarios/{iid}/movimientos/",
                json={"tipo": tipo, "cantidad": cant, "notas": notas, "usuario_id": int(uid) if uid else None},
            )
            flash("Movimiento registrado.", "success")
        except ApiError as e:
            flash(str(e.message), "danger")
        return redirect(url_for("almacen_inventario"))

    @app.route("/almacen/ubicaciones", methods=["GET", "POST"])
    def almacen_ubicaciones():
        redir = solo_almacen()
        if redir:
            return redir
        api = get_api()
        if request.method == "POST":
            act = request.form.get("_action")
            if act == "nueva":
                ok, msg, pas = validate_short_text(request.form.get("pasillo"), "Pasillo", 40)
                if not ok:
                    flash(msg, "danger")
                    return redirect(url_for("almacen_ubicaciones"))
                ok, msg, est = validate_short_text(request.form.get("estante"), "Estante", 40)
                if not ok:
                    flash(msg, "danger")
                    return redirect(url_for("almacen_ubicaciones"))
                nivel = (request.form.get("nivel") or "").strip()[:20] or None
                ok_c, err_c, cap = validate_int(
                    request.form.get("capacidad"), "Capacidad", min_v=0, max_v=10_000_000
                )
                capacidad = int(cap) if ok_c else None
                if request.form.get("capacidad") and not ok_c:
                    flash(err_c, "danger")
                    return redirect(url_for("almacen_ubicaciones"))
                desc = (request.form.get("descripcion") or "").strip()[:500] or None
                try:
                    api.post(
                        "/v1/ubicaciones/",
                        json={
                            "pasillo": pas,
                            "estante": est,
                            "nivel": nivel,
                            "capacidad": capacidad,
                            "descripcion": desc,
                            "activo": True,
                        },
                    )
                    flash("Ubicación creada.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "editar":
                ok, err, uid = validate_int(request.form.get("ubicacion_id"), "Ubicación")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("almacen_ubicaciones"))
                body = {}
                if request.form.get("capacidad"):
                    ok_c, err_c, cap = validate_int(
                        request.form.get("capacidad"), "Capacidad", min_v=0, max_v=10_000_000
                    )
                    if not ok_c:
                        flash(err_c, "danger")
                        return redirect(url_for("almacen_ubicaciones"))
                    body["capacidad"] = int(cap)
                if request.form.get("descripcion") is not None:
                    body["descripcion"] = (request.form.get("descripcion") or "").strip()[:500] or None
                if request.form.get("pasillo"):
                    body["pasillo"] = request.form.get("pasillo", "").strip()[:40]
                if request.form.get("estante"):
                    body["estante"] = request.form.get("estante", "").strip()[:40]
                if not body:
                    flash("Sin cambios.", "warning")
                    return redirect(url_for("almacen_ubicaciones"))
                try:
                    api.put(f"/v1/ubicaciones/{uid}", json=body)
                    flash("Ubicación actualizada.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "eliminar":
                ok, err, uid = validate_int(request.form.get("ubicacion_id"), "Ubicación")
                if ok:
                    try:
                        api.delete(f"/v1/ubicaciones/{uid}")
                        flash("Ubicación eliminada.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(err, "danger")
            return redirect(url_for("almacen_ubicaciones"))

        try:
            ubicaciones = api.get("/v1/ubicaciones/")
        except ApiError as e:
            flash(str(e.message), "danger")
            ubicaciones = []
        return render_template("almacen_ubicaciones.html", ubicaciones=ubicaciones)

    @app.route("/almacen/pedidos", methods=["GET"])
    def almacen_pedidos():
        redir = solo_almacen()
        if redir:
            return redir
        api = get_api()
        try:
            pedidos = api.get("/v1/pedidos/")
            pedidos_e = _enriquecer_pedidos(api, pedidos)
        except ApiError as e:
            flash(str(e.message), "danger")
            pedidos_e = []
        return render_template("almacen_pedidos.html", pedidos=pedidos_e)

    @app.route("/almacen/pedidos/<int:pedido_id>/estatus", methods=["POST"])
    def almacen_pedidos_estatus(pedido_id):
        redir = solo_almacen()
        if redir:
            return redir
        nombre = (request.form.get("estatus") or "").strip()
        if nombre not in ("Surtiendo", "Empacado"):
            flash("Estatus no permitido para almacén.", "danger")
            return redirect(url_for("almacen_pedidos"))
        api = get_api()
        eid = api_helpers.estatus_por_nombre(api, nombre)
        if not eid:
            flash("Estatus no encontrado.", "danger")
            return redirect(url_for("almacen_pedidos"))
        try:
            api.patch(f"/v1/pedidos/{pedido_id}/estatus", json={"estatus_id": eid})
            flash(f"Pedido en «{nombre}».", "success")
        except ApiError as e:
            flash(str(e.message), "danger")
        return redirect(url_for("almacen_pedidos"))

    @app.route("/almacen/autopartes")
    def almacen_autopartes():
        redir = solo_almacen()
        if redir:
            return redir
        api = get_api()
        try:
            autopartes = api.get("/v1/autopartes/")
            categorias = {c["id"]: c.get("nombre") for c in api.get("/v1/categorias/")}
            marcas = {m["id"]: m.get("nombre") for m in api.get("/v1/marcas/")}
            for a in autopartes:
                a["_cat"] = categorias.get(a.get("categoria_id"), "")
                a["_marca"] = marcas.get(a.get("marca_id"), "")
        except ApiError as e:
            flash(str(e.message), "danger")
            autopartes = []
        return render_template("almacen_autopartes.html", autopartes=autopartes)
