"""Módulo Ventas: clientes, pedidos y catálogo contra la API."""

from __future__ import annotations

from typing import Dict, List

from flask import flash, redirect, render_template, request, session, url_for

from routes import api_helpers
from services.api import ApiError, get_api
from services.stats import conteo_estatus_pedidos, totales_pedidos_por_mes, ventas_kpis
from services.validators import (
    require_non_empty,
    validate_cp_mx,
    validate_email,
    validate_int,
    validate_phone,
    validate_short_text,
)


def register(app):
    def requiere_login():
        return "user_id" not in session

    def solo_ventas():
        if requiere_login():
            return redirect(url_for("login"))
        if session.get("user_role") != "Ventas":
            return redirect(url_for("index"))
        return None

    def _estatus_map(api) -> Dict[int, str]:
        try:
            lst = api.get("/v1/estatus-pedido/")
            return {int(e["id"]): (e.get("nombre") or "") for e in lst}
        except ApiError:
            return {}

    def _enriquecer_pedidos(api, pedidos: List[dict]) -> List[dict]:
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
            fd = p.get("fecha_pedido")
            if fd:
                try:
                    s = str(fd).replace("Z", "+00:00")
                    dt = datetime.fromisoformat(s)
                    q["_fecha_corta"] = dt.strftime("%d/%m/%Y")
                except ValueError:
                    q["_fecha_corta"] = str(fd)[:10]
            else:
                q["_fecha_corta"] = "—"
            try:
                q["_total_fmt"] = f"${float(p.get('total') or 0):,.2f}"
            except (TypeError, ValueError):
                q["_total_fmt"] = str(p.get("total"))
            out.append(q)
        return out

    def _pedido_cerrado_o_enviado(nombre_estatus: str) -> bool:
        return nombre_estatus in ("Enviado", "Entregado", "Cancelado")

    @app.route("/ventas")
    @app.route("/ventas/dashboard")
    def ventas_dashboard():
        redir = solo_ventas()
        if redir:
            return redir
        api = get_api()
        try:
            clientes = api.get("/v1/clientes/")
            pedidos = api.get("/v1/pedidos/")
            estatus = api.get("/v1/estatus-pedido/")
            kpis = ventas_kpis(pedidos, clientes)
            lbl_m, dat_m = totales_pedidos_por_mes(pedidos)
            lbl_e, dat_e = conteo_estatus_pedidos(pedidos, estatus)
            recientes = _enriquecer_pedidos(api, pedidos[:8])
            ventas_acumulado = sum(float(p.get("total") or 0) for p in pedidos)
        except ApiError as e:
            flash(str(e.message), "danger")
            kpis = {}
            lbl_m, dat_m, lbl_e, dat_e = [], [], [], []
            recientes = []
            ventas_acumulado = 0.0
        return render_template(
            "ventas_dashboard.html",
            kpi=kpis,
            chart_mes_labels=lbl_m,
            chart_mes_data=dat_m,
            chart_estatus_labels=lbl_e,
            chart_estatus_data=dat_e,
            pedidos_recientes=recientes,
            ventas_acumulado=ventas_acumulado,
        )

    @app.route("/ventas/clientes", methods=["GET", "POST"])
    def ventas_clientes():
        redir = solo_ventas()
        if redir:
            return redir
        api = get_api()
        if request.method == "POST":
            act = request.form.get("_action")
            if act == "nuevo":
                ok, msg = require_non_empty(request.form.get("nombre"), "Nombre / empresa")
                if not ok:
                    flash(msg, "danger")
                    return redirect(url_for("ventas_clientes"))
                ok, em = validate_email(request.form.get("correo"))
                if not ok:
                    flash(em, "danger")
                    return redirect(url_for("ventas_clientes"))
                ok_tel, tel = validate_phone(request.form.get("telefono"))
                if not ok_tel:
                    flash(tel, "danger")
                    return redirect(url_for("ventas_clientes"))
                notas = (request.form.get("notas") or "").strip()[:2000] or None
                try:
                    api.post(
                        "/v1/clientes/",
                        json={
                            "nombre": request.form.get("nombre", "").strip()[:200],
                            "email": em,
                            "telefono": tel or None,
                            "activo": True,
                            "notas": notas,
                        },
                    )
                    flash("Cliente registrado.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "editar":
                ok, err, cid = validate_int(request.form.get("cliente_id"), "ID cliente")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("ventas_clientes"))
                ok, em = validate_email(request.form.get("correo"))
                if not ok:
                    flash(em, "danger")
                    return redirect(url_for("ventas_clientes"))
                try:
                    api.put(f"/v1/clientes/{cid}", json={"email": em})
                    flash("Correo actualizado.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "baja":
                ok, err, cid = validate_int(request.form.get("cliente_id"), "ID cliente")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("ventas_clientes"))
                try:
                    api.patch(f"/v1/clientes/{cid}/baja", json={})
                    flash("Cliente dado de baja (inactivo).", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            return redirect(url_for("ventas_clientes"))

        try:
            clientes = api.get("/v1/clientes/")
            total = len(clientes)
            activos = sum(1 for c in clientes if c.get("activo", True))
        except ApiError as e:
            flash(str(e.message), "danger")
            clientes, total, activos = [], 0, 0
        return render_template(
            "ventas_clientes.html",
            clientes=clientes,
            total_clientes=total,
            clientes_activos=activos,
            clientes_baja=total - activos,
        )

    @app.route("/ventas/pedidos", methods=["GET"])
    def ventas_pedidos():
        redir = solo_ventas()
        if redir:
            return redir
        api = get_api()
        try:
            pedidos = api.get("/v1/pedidos/")
            pedidos = pedidos[:150]
            estatus = api.get("/v1/estatus-pedido/")
            clientes = api.get("/v1/clientes/")
            autopartes = api.get("/v1/autopartes/")
            id_est = {e["id"]: e.get("nombre", "") for e in estatus}
            pedidos_e = _enriquecer_pedidos(api, pedidos)
            for p in pedidos_e:
                try:
                    detalles = api.get(f"/v1/pedidos/{p['id']}/detalles")
                    p["_num_lineas"] = len(detalles) if isinstance(detalles, list) else 0
                except ApiError:
                    p["_num_lineas"] = 0
            enviados = sum(1 for p in pedidos if id_est.get(p.get("estatus_id")) == "Enviado")
            entregados = sum(1 for p in pedidos if id_est.get(p.get("estatus_id")) == "Entregado")
            proceso = sum(
                1
                for p in pedidos
                if id_est.get(p.get("estatus_id"))
                not in ("Enviado", "Entregado", "Cancelado")
            )
            cancelados = sum(1 for p in pedidos if p.get("motivo_cancelacion"))
            estatus_opciones = sorted(
                {p.get("_estatus_nombre") or "" for p in pedidos_e if p.get("_estatus_nombre")}
            )
        except ApiError as e:
            flash(str(e.message), "danger")
            pedidos_e, clientes, autopartes = [], [], []
            enviados = entregados = proceso = cancelados = 0
            estatus_opciones = []
        return render_template(
            "ventas_pedidos.html",
            pedidos=pedidos_e,
            clientes=clientes,
            autopartes=autopartes,
            kpi_total=len(pedidos_e),
            kpi_enviados=enviados,
            kpi_proceso=proceso,
            kpi_cancelados=cancelados,
            estatus_opciones=estatus_opciones,
        )

    @app.route("/ventas/pedidos/nuevo", methods=["POST"])
    def ventas_pedido_nuevo():
        redir = solo_ventas()
        if redir:
            return redir
        api = get_api()
        ok, err, cliente_id = validate_int(request.form.get("cliente_id"), "Cliente")
        if not ok:
            flash(err, "danger")
            return redirect(url_for("ventas_pedidos"))
        ok, msg, calle = validate_short_text(request.form.get("calle_principal"), "Calle", 150)
        if not ok:
            flash(msg, "danger")
            return redirect(url_for("ventas_pedidos"))
        ok, msg, num_ext = validate_short_text(request.form.get("num_ext"), "Número exterior", 10)
        if not ok:
            flash(msg, "danger")
            return redirect(url_for("ventas_pedidos"))
        ok, msg, colonia = validate_short_text(request.form.get("colonia"), "Colonia", 100)
        if not ok:
            flash(msg, "danger")
            return redirect(url_for("ventas_pedidos"))
        ok, msg, municipio = validate_short_text(request.form.get("municipio"), "Municipio", 100)
        if not ok:
            flash(msg, "danger")
            return redirect(url_for("ventas_pedidos"))
        ok, msg, estado = validate_short_text(request.form.get("estado"), "Estado", 100)
        if not ok:
            flash(msg, "danger")
            return redirect(url_for("ventas_pedidos"))
        ok, cp = validate_cp_mx(request.form.get("cp"))
        if not ok:
            flash(cp, "danger")
            return redirect(url_for("ventas_pedidos"))
        num_int = (request.form.get("num_int") or "").strip()[:10] or None
        referencias = (request.form.get("referencias") or "").strip()[:500] or None

        ids = request.form.getlist("autoparte_id")
        cants = request.form.getlist("cantidad")
        lineas: List[tuple[int, int]] = []
        for aid_s, c_s in zip(ids, cants):
            ok_a, e_a, aid = validate_int(aid_s, "Autoparte")
            ok_c, e_c, cant = validate_int(c_s, "Cantidad", min_v=1, max_v=99999)
            if ok_a and ok_c:
                lineas.append((aid, cant))
            elif not ok_a:
                flash(e_a, "danger")
                return redirect(url_for("ventas_pedidos"))
            elif not ok_c:
                flash(e_c, "danger")
                return redirect(url_for("ventas_pedidos"))
        if not lineas:
            flash("Agrega al menos una línea con autoparte y cantidad.", "danger")
            return redirect(url_for("ventas_pedidos"))

        eid = api_helpers.estatus_por_nombre(api, "Pendiente") or api_helpers.estatus_por_nombre(api, "Confirmado")
        if not eid:
            flash("No se encontró estatus inicial de pedido en el sistema.", "danger")
            return redirect(url_for("ventas_pedidos"))

        try:
            dir_body = {
                "calle_principal": calle,
                "num_ext": num_ext,
                "num_int": num_int,
                "colonia": colonia,
                "municipio": municipio,
                "estado": estado,
                "cp": cp,
                "referencias": referencias,
                "cliente_id": cliente_id,
            }
            nueva_dir = api.post("/v1/direcciones/", json=dir_body)
            did = int(nueva_dir["id"])

            total = 0.0
            precios_lineas: List[tuple[int, int, float]] = []
            for aid, cant in lineas:
                ap = api.get(f"/v1/autopartes/{aid}")
                precio = float(ap.get("precio_unitario") or 0)
                total += precio * cant
                precios_lineas.append((aid, cant, precio))

            ped = api.post(
                "/v1/pedidos/",
                json={
                    "folio": None,
                    "usuario_id": int(session["user_id"]),
                    "estatus_id": eid,
                    "total": round(total, 2),
                    "direccion_envio_id": did,
                    "cliente_id": cliente_id,
                    "motivo_cancelacion": None,
                    "fecha_cancelacion": None,
                },
            )
            pid = int(ped["id"])
            for aid, cant, precio in precios_lineas:
                api.post(
                    f"/v1/pedidos/{pid}/detalles",
                    json={"autoparte_id": aid, "cantidad": cant, "precio_historico": precio},
                )
            flash(f"Pedido #{pid} creado correctamente.", "success")
        except ApiError as e:
            flash(str(e.message), "danger")
        return redirect(url_for("ventas_pedidos"))

    @app.route("/ventas/pedidos/<int:pedido_id>/editar", methods=["POST"])
    def ventas_pedido_editar(pedido_id):
        redir = solo_ventas()
        if redir:
            return redir
        api = get_api()
        accion = (request.form.get("accion") or "").strip().lower()
        try:
            p = api.get(f"/v1/pedidos/{pedido_id}")
        except ApiError as e:
            flash(str(e.message), "danger")
            return redirect(url_for("ventas_pedidos"))
        id_est = _estatus_map(api)
        nom = id_est.get(int(p.get("estatus_id") or 0), "")

        if accion == "cancelar":
            if _pedido_cerrado_o_enviado(nom) or p.get("motivo_cancelacion"):
                flash("Este pedido no admite cancelación.", "danger")
                return redirect(url_for("ventas_pedidos"))
            ok, motivo = require_non_empty(request.form.get("motivo_cancelacion"), "Motivo de cancelación")
            if not ok:
                flash(motivo, "danger")
                return redirect(url_for("ventas_pedidos"))
            try:
                api.patch(
                    f"/v1/pedidos/{pedido_id}/cancelar",
                    json={"motivo_cancelacion": motivo[:2000]},
                )
                flash("Pedido cancelado.", "warning")
            except ApiError as e:
                flash(str(e.message), "danger")
            return redirect(url_for("ventas_pedidos"))

        if accion == "direccion":
            if _pedido_cerrado_o_enviado(nom) or p.get("motivo_cancelacion"):
                flash("No se puede cambiar la dirección en el estado actual.", "danger")
                return redirect(url_for("ventas_pedidos"))
            ok, msg, calle = validate_short_text(request.form.get("calle_principal"), "Calle", 150)
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("ventas_pedidos"))
            ok, msg, num_ext = validate_short_text(request.form.get("num_ext"), "Número exterior", 10)
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("ventas_pedidos"))
            ok, msg, colonia = validate_short_text(request.form.get("colonia"), "Colonia", 100)
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("ventas_pedidos"))
            ok, msg, municipio = validate_short_text(request.form.get("municipio"), "Municipio", 100)
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("ventas_pedidos"))
            ok, msg, estado = validate_short_text(request.form.get("estado"), "Estado", 100)
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("ventas_pedidos"))
            ok, cp = validate_cp_mx(request.form.get("cp"))
            if not ok:
                flash(cp, "danger")
                return redirect(url_for("ventas_pedidos"))
            num_int = (request.form.get("num_int") or "").strip()[:10] or None
            referencias = (request.form.get("referencias") or "").strip()[:500] or None
            try:
                nueva_dir = api.post(
                    "/v1/direcciones/",
                    json={
                        "calle_principal": calle,
                        "num_ext": num_ext,
                        "num_int": num_int,
                        "colonia": colonia,
                        "municipio": municipio,
                        "estado": estado,
                        "cp": cp,
                        "referencias": referencias,
                        "cliente_id": p.get("cliente_id"),
                    },
                )
                did = int(nueva_dir["id"])
                api.put(
                    f"/v1/pedidos/{pedido_id}",
                    json={
                        "folio": p.get("folio"),
                        "usuario_id": p["usuario_id"],
                        "estatus_id": p["estatus_id"],
                        "total": float(p.get("total") or 0),
                        "direccion_envio_id": did,
                        "cliente_id": p.get("cliente_id"),
                        "motivo_cancelacion": p.get("motivo_cancelacion"),
                        "fecha_cancelacion": p.get("fecha_cancelacion"),
                    },
                )
                flash("Dirección de entrega actualizada.", "success")
            except ApiError as e:
                flash(str(e.message), "danger")
            return redirect(url_for("ventas_pedidos"))

        flash("Acción no reconocida.", "danger")
        return redirect(url_for("ventas_pedidos"))

    @app.route("/ventas/catalogo")
    def ventas_catalogo():
        redir = solo_ventas()
        if redir:
            return redir
        api = get_api()
        try:
            autopartes = api.get("/v1/autopartes/")
            categorias = {c["id"]: c.get("nombre") for c in api.get("/v1/categorias/")}
            marcas = {m["id"]: m.get("nombre") for m in api.get("/v1/marcas/")}
            inv = api.get("/v1/inventarios/")
            by_ap: Dict[int, int] = {}
            for i in inv:
                aid = i.get("autoparte_id")
                if aid is not None:
                    by_ap[int(aid)] = by_ap.get(int(aid), 0) + int(i.get("stock_actual") or 0)
            cats_set = set()
            for a in autopartes:
                a["_cat"] = categorias.get(a.get("categoria_id"), "")
                a["_marca"] = marcas.get(a.get("marca_id"), "")
                st = by_ap.get(int(a["id"]), 0)
                a["_stock_total"] = st
                if a["_cat"]:
                    cats_set.add(a["_cat"])
                if st > 10:
                    a["_nivel"] = "disponible"
                elif st >= 1:
                    a["_nivel"] = "bajo"
                else:
                    a["_nivel"] = "agotado"
            categorias_distintas = sorted(cats_set)
        except ApiError as e:
            flash(str(e.message), "danger")
            autopartes = []
            categorias_distintas = []
        return render_template(
            "ventas_catalogo.html",
            autopartes=autopartes,
            categorias_distintas=categorias_distintas,
        )
