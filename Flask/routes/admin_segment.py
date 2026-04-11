import bcrypt
from collections import defaultdict

from flask import flash, redirect, render_template, request, session, url_for

from routes import api_helpers
from services.api import ApiError, get_api
from services.stats import admin_kpis, conteo_roles, pedidos_por_mes
from services.validators import (
    require_non_empty,
    validate_email,
    validate_float,
    validate_int,
    validate_password_plain,
    validate_phone,
    validate_short_text,
    validate_sku,
)


def register(app):
    def requiere_login():
        return "user_id" not in session

    def requiere_rol(rol):
        return session.get("user_role") != rol

    def solo_admin():
        if requiere_login():
            return redirect(url_for("login"))
        if requiere_rol("Administrador"):
            return redirect(url_for("index"))
        return None

    @app.context_processor
    def _inject_portal_contacto_unread():
        if "user_id" not in session or session.get("user_role") != "Administrador":
            return {"portal_contacto_unread": 0}
        try:
            api = get_api()
            c = api.get("/v1/portal-contacto/mensajes/no-leidos/count")
            n = int(c.get("count", 0)) if isinstance(c, dict) else 0
            return {"portal_contacto_unread": n}
        except Exception:
            return {"portal_contacto_unread": 0}

    @app.route("/admin")
    @app.route("/admin/dashboard")
    def admin_dashboard():
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        try:
            raw_u = api.get("/v1/usuarios/")
            usuarios = raw_u.get("usuarios", []) if isinstance(raw_u, dict) else []
            pedidos = api.get("/v1/pedidos/")
            autopartes = api.get("/v1/autopartes/")
            parametros = api.get("/v1/parametros-sistema/")
            kpis = admin_kpis(usuarios, autopartes, pedidos, parametros)
            lbl_m, dat_m = pedidos_por_mes(pedidos)
            lbl_r, dat_r = conteo_roles(usuarios, api.get("/v1/roles/"))
            actividades = api.get("/v1/pedidos/admin/vista", params={"limit": 12})
            if not isinstance(actividades, list):
                actividades = []
        except ApiError as e:
            flash(f"No se pudo cargar el panel: {e.message}", "danger")
            kpis = {}
            lbl_m, dat_m, lbl_r, dat_r = [], [], [], []
            actividades = []
        return render_template(
            "admin_dashboard.html",
            kpi=kpis,
            chart_pedidos_labels=lbl_m,
            chart_pedidos_data=dat_m,
            chart_roles_labels=lbl_r,
            chart_roles_data=dat_r,
            actividades_recientes=actividades,
        )

    @app.route("/admin/usuarios", methods=["GET", "POST"])
    def admin_usuarios():
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        if request.method == "POST" and request.form.get("_action") == "nuevo":
            ok, msg = require_non_empty(request.form.get("nombre"), "Nombre")
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("admin_usuarios"))
            ok, msg = require_non_empty(request.form.get("apellidos"), "Apellidos")
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("admin_usuarios"))
            ok, em = validate_email(request.form.get("correo"))
            if not ok:
                flash(em, "danger")
                return redirect(url_for("admin_usuarios"))
            ok, pw = validate_password_plain(request.form.get("password"), min_len=6)
            if not ok:
                flash(pw, "danger")
                return redirect(url_for("admin_usuarios"))
            ok, tel = validate_phone(request.form.get("telefono"))
            if not ok:
                flash(tel, "danger")
                return redirect(url_for("admin_usuarios"))
            rid = api_helpers.rol_por_nombre(api, request.form.get("rol", "").strip())
            if not rid:
                flash("Rol no válido.", "danger")
                return redirect(url_for("admin_usuarios"))
            h = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            try:
                api.post(
                    "/v1/usuarios/",
                    json={
                        "nombre": request.form.get("nombre", "").strip()[:100],
                        "apellidos": request.form.get("apellidos", "").strip()[:150],
                        "email": em,
                        "password_hash": h,
                        "telefono": tel or None,
                        "rol_id": rid,
                        "direccion_id": None,
                        "activo": True,
                    },
                )
                flash("Usuario creado.", "success")
            except ApiError as e:
                flash(str(e.message), "danger")
            return redirect(url_for("admin_usuarios"))

        if request.method == "POST" and request.form.get("_action") == "editar":
            ok, msg, uid = validate_int(request.form.get("usuario_id"), "ID usuario")
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("admin_usuarios"))
            ok, em = validate_email(request.form.get("correo"))
            if not ok:
                flash(em, "danger")
                return redirect(url_for("admin_usuarios"))
            rid = api_helpers.rol_por_nombre(api, request.form.get("rol", "").strip())
            if not rid:
                flash("Rol no válido.", "danger")
                return redirect(url_for("admin_usuarios"))
            u = api.get(f"/v1/usuarios/{uid}")
            ok_tel, tel = validate_phone(request.form.get("telefono"))
            if not ok_tel:
                flash(tel, "danger")
                return redirect(url_for("admin_usuarios"))
            try:
                api.put(
                    f"/v1/usuarios/{uid}",
                    json={
                        "nombre": request.form.get("nombre", "").strip()[:100],
                        "apellidos": request.form.get("apellidos", "").strip()[:150],
                        "email": em,
                        "password_hash": u["password_hash"],
                        "telefono": tel or None,
                        "rol_id": rid,
                        "direccion_id": u.get("direccion_id"),
                        "activo": bool(u.get("activo", True)),
                    },
                )
                flash("Usuario actualizado.", "success")
            except ApiError as e:
                flash(str(e.message), "danger")
            return redirect(url_for("admin_usuarios"))

        if request.method == "POST" and request.form.get("_action") == "reset_pass":
            ok, msg, uid = validate_int(request.form.get("usuario_id"), "ID usuario")
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("admin_usuarios"))
            ok, pw = validate_password_plain(request.form.get("password"), min_len=6)
            if not ok:
                flash(pw, "danger")
                return redirect(url_for("admin_usuarios"))
            u = api.get(f"/v1/usuarios/{uid}")
            h = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            try:
                api.put(
                    f"/v1/usuarios/{uid}",
                    json={
                        "nombre": u["nombre"],
                        "apellidos": u["apellidos"],
                        "email": u["email"],
                        "password_hash": h,
                        "telefono": u.get("telefono"),
                        "rol_id": u["rol_id"],
                        "direccion_id": u.get("direccion_id"),
                        "activo": u.get("activo", True),
                    },
                )
                flash("Contraseña actualizada.", "success")
            except ApiError as e:
                flash(str(e.message), "danger")
            return redirect(url_for("admin_usuarios"))

        if request.method == "POST" and request.form.get("_action") == "baja":
            ok, msg, uid = validate_int(request.form.get("usuario_id"), "ID usuario")
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("admin_usuarios"))
            u = api.get(f"/v1/usuarios/{uid}")
            try:
                api.put(
                    f"/v1/usuarios/{uid}",
                    json={
                        "nombre": u["nombre"],
                        "apellidos": u["apellidos"],
                        "email": u["email"],
                        "password_hash": u["password_hash"],
                        "telefono": u.get("telefono"),
                        "rol_id": u["rol_id"],
                        "direccion_id": u.get("direccion_id"),
                        "activo": False,
                    },
                )
                flash("Usuario dado de baja.", "success")
            except ApiError as e:
                flash(str(e.message), "danger")
            return redirect(url_for("admin_usuarios"))

        if request.method == "POST" and request.form.get("_action") == "reactivar":
            ok, msg, uid = validate_int(request.form.get("usuario_id"), "ID usuario")
            if not ok:
                flash(msg, "danger")
                return redirect(url_for("admin_usuarios"))
            u = api.get(f"/v1/usuarios/{uid}")
            try:
                api.put(
                    f"/v1/usuarios/{uid}",
                    json={
                        "nombre": u["nombre"],
                        "apellidos": u["apellidos"],
                        "email": u["email"],
                        "password_hash": u["password_hash"],
                        "telefono": u.get("telefono"),
                        "rol_id": u["rol_id"],
                        "direccion_id": u.get("direccion_id"),
                        "activo": True,
                    },
                )
                flash("Usuario reactivado.", "success")
            except ApiError as e:
                flash(str(e.message), "danger")
            return redirect(url_for("admin_usuarios"))

        try:
            raw = api.get("/v1/usuarios/")
            usuarios = raw.get("usuarios", []) if isinstance(raw, dict) else []
            roles = api.get("/v1/roles/")
            id_rol = {int(r["id"]): r.get("nombre_rol", "") for r in roles}
            for u in usuarios:
                u["_rol_nombre"] = id_rol.get(int(u.get("rol_id") or 0), "")
        except ApiError as e:
            flash(str(e.message), "danger")
            usuarios, roles = [], []
        return render_template("admin_usuarios.html", usuarios=usuarios, roles=roles)

    @app.route("/admin/catalogo", methods=["GET", "POST"])
    def admin_catalogo():
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        if request.method == "POST":
            act = request.form.get("_action")
            if act == "nuevo":
                ok, sku = validate_sku(request.form.get("sku_codigo"))
                if not ok:
                    flash(sku, "danger")
                    return redirect(url_for("admin_catalogo"))
                ok, msg = require_non_empty(request.form.get("nombre"), "Nombre")
                if not ok:
                    flash(msg, "danger")
                    return redirect(url_for("admin_catalogo"))
                cid = api_helpers.categoria_por_nombre(api, request.form.get("categoria", "").strip())
                mid = api_helpers.marca_por_nombre(api, request.form.get("marca", "").strip())
                if not cid or not mid:
                    flash("Categoría o marca no encontrada en el catálogo maestro.", "danger")
                    return redirect(url_for("admin_catalogo"))
                ok, err, precio = validate_float(request.form.get("precio"), "Precio", min_v=0.01)
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("admin_catalogo"))
                try:
                    api.post(
                        "/v1/autopartes/",
                        json={
                            "sku_codigo": sku,
                            "nombre": request.form.get("nombre", "").strip()[:150],
                            "descripcion": (request.form.get("descripcion") or "").strip() or None,
                            "precio_unitario": float(precio),
                            "imagen_url": None,
                            "categoria_id": cid,
                            "marca_id": mid,
                        },
                    )
                    flash("Autoparte creada.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "editar":
                ok, err, aid = validate_int(request.form.get("autoparte_id"), "ID autoparte")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("admin_catalogo"))
                cid = api_helpers.categoria_por_nombre(api, request.form.get("categoria", "").strip())
                mid = api_helpers.marca_por_nombre(api, request.form.get("marca", "").strip())
                ok, errp, precio = validate_float(request.form.get("precio"), "Precio", min_v=0.01)
                if not (cid and mid and ok):
                    flash("Datos inválidos o precio incorrecto.", "danger")
                    return redirect(url_for("admin_catalogo"))
                cur = api.get(f"/v1/autopartes/{aid}")
                try:
                    api.put(
                        f"/v1/autopartes/{aid}",
                        json={
                            "sku_codigo": cur["sku_codigo"],
                            "nombre": request.form.get("nombre", "").strip()[:150],
                            "descripcion": (request.form.get("descripcion") or "").strip() or None,
                            "precio_unitario": float(precio),
                            "imagen_url": cur.get("imagen_url"),
                            "categoria_id": cid,
                            "marca_id": mid,
                        },
                    )
                    flash("Autoparte actualizada.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "eliminar":
                ok, err, aid = validate_int(request.form.get("autoparte_id"), "ID autoparte")
                if ok:
                    try:
                        api.delete(f"/v1/autopartes/{aid}")
                        flash("Autoparte eliminada.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(err, "danger")
            elif act == "nueva_categoria":
                ok, msg, nom = validate_short_text(
                    request.form.get("nombre"), "Nombre de categoría", 100
                )
                if ok:
                    try:
                        api.post("/v1/categorias/", json={"nombre": nom})
                        flash("Categoría creada.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(msg, "danger")
            elif act == "editar_categoria":
                ok, err, cid = validate_int(request.form.get("categoria_id"), "Categoría")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("admin_catalogo"))
                ok, msg, nom = validate_short_text(
                    request.form.get("nombre"), "Nombre de categoría", 100
                )
                if ok:
                    try:
                        api.put(f"/v1/categorias/{cid}", json={"nombre": nom})
                        flash("Categoría actualizada.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(msg, "danger")
            elif act == "eliminar_categoria":
                ok, err, cid = validate_int(request.form.get("categoria_id"), "Categoría")
                if ok:
                    try:
                        api.delete(f"/v1/categorias/{cid}")
                        flash("Categoría eliminada.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(err, "danger")
            return redirect(url_for("admin_catalogo"))

        try:
            autopartes = api.get("/v1/autopartes/")
            categorias = api.get("/v1/categorias/")
            marcas = api.get("/v1/marcas/")
            cat_map = {c["id"]: c.get("nombre", "") for c in categorias}
            mar_map = {m["id"]: m.get("nombre", "") for m in marcas}
            counts: dict = {}
            for a in autopartes:
                cid = a.get("categoria_id")
                if cid:
                    counts[cid] = counts.get(cid, 0) + 1
            for c in categorias:
                c["_count_autopartes"] = counts.get(c["id"], 0)
            for a in autopartes:
                a["_cat"] = cat_map.get(a.get("categoria_id"), "")
                a["_marca"] = mar_map.get(a.get("marca_id"), "")
        except ApiError as e:
            flash(str(e.message), "danger")
            autopartes, categorias, marcas = [], [], []
        return render_template(
            "admin_catalogo.html",
            autopartes=autopartes,
            categorias=categorias,
            marcas=marcas,
        )

    @app.route("/admin/configuracion", methods=["GET", "POST"])
    def admin_configuracion():
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        if request.method == "POST":
            act = request.form.get("_action")
            if act == "nuevo_rol":
                ok, n = require_non_empty(request.form.get("nombre_rol"), "Nombre del rol")
                if ok:
                    try:
                        api.post(
                            "/v1/roles/",
                            json={
                                "nombre_rol": n[:30],
                                "descripcion": (request.form.get("descripcion") or "").strip() or None,
                                "permisos": (request.form.get("permisos") or "").strip() or None,
                            },
                        )
                        flash("Rol creado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
            elif act == "nuevo_estatus":
                ok, n = require_non_empty(request.form.get("nombre_estatus"), "Nombre estatus")
                if ok:
                    try:
                        api.post(
                            "/v1/estatus-pedido/",
                            json={
                                "nombre": n[:50],
                                "modulo": (request.form.get("modulo") or "").strip() or None,
                                "color": (request.form.get("color") or "").strip() or None,
                            },
                        )
                        flash("Estatus creado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
            elif act == "nuevo_param":
                ok, c = require_non_empty(request.form.get("clave"), "Clave")
                ok2, v = require_non_empty(request.form.get("valor"), "Valor")
                if ok and ok2:
                    try:
                        api.post(
                            "/v1/parametros-sistema/",
                            json={
                                "tipo": (request.form.get("tipo_param") or "parametro")[:40],
                                "clave": c[:120],
                                "valor": v,
                                "descripcion": (request.form.get("descripcion") or "").strip() or None,
                                "activo": True,
                            },
                        )
                        flash("Parámetro creado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
            elif act == "editar_rol":
                ok, err, rid = validate_int(request.form.get("rol_id"), "Rol")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("admin_configuracion"))
                ok, n = require_non_empty(request.form.get("nombre_rol"), "Nombre del rol")
                if ok:
                    try:
                        api.put(
                            f"/v1/roles/{rid}",
                            json={
                                "nombre_rol": request.form.get("nombre_rol", "").strip()[:30],
                                "descripcion": (request.form.get("descripcion") or "").strip() or None,
                                "permisos": (request.form.get("permisos") or "").strip() or None,
                            },
                        )
                        flash("Rol actualizado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(n, "danger")
            elif act == "eliminar_rol":
                ok, err, rid = validate_int(request.form.get("rol_id"), "Rol")
                if ok:
                    try:
                        api.delete(f"/v1/roles/{rid}")
                        flash("Rol eliminado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(err, "danger")
            elif act == "editar_estatus":
                ok, err, eid = validate_int(request.form.get("estatus_id"), "Estatus")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("admin_configuracion"))
                ok, n = require_non_empty(request.form.get("nombre_estatus"), "Nombre estatus")
                if ok:
                    try:
                        api.put(
                            f"/v1/estatus-pedido/{eid}",
                            json={
                                "nombre": request.form.get("nombre_estatus", "").strip()[:50],
                                "modulo": (request.form.get("modulo") or "").strip() or None,
                                "color": (request.form.get("color") or "").strip() or None,
                            },
                        )
                        flash("Estatus actualizado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(n, "danger")
            elif act == "eliminar_estatus":
                ok, err, eid = validate_int(request.form.get("estatus_id"), "Estatus")
                if ok:
                    try:
                        api.delete(f"/v1/estatus-pedido/{eid}")
                        flash("Estatus eliminado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(err, "danger")
            elif act == "editar_param":
                ok, err, pid = validate_int(request.form.get("parametro_id"), "Parámetro")
                if not ok:
                    flash(err, "danger")
                    return redirect(url_for("admin_configuracion"))
                body = {}
                if request.form.get("valor") is not None:
                    body["valor"] = (request.form.get("valor") or "").strip()
                if request.form.get("descripcion") is not None:
                    body["descripcion"] = (request.form.get("descripcion") or "").strip() or None
                if request.form.get("activo") == "1":
                    body["activo"] = True
                elif request.form.get("activo") == "0":
                    body["activo"] = False
                if not body:
                    flash("Sin cambios.", "warning")
                    return redirect(url_for("admin_configuracion"))
                try:
                    api.put(f"/v1/parametros-sistema/{pid}", json=body)
                    flash("Parámetro actualizado.", "success")
                except ApiError as e:
                    flash(str(e.message), "danger")
            elif act == "eliminar_param":
                ok, err, pid = validate_int(request.form.get("parametro_id"), "Parámetro")
                if ok:
                    try:
                        api.delete(f"/v1/parametros-sistema/{pid}")
                        flash("Parámetro eliminado.", "success")
                    except ApiError as e:
                        flash(str(e.message), "danger")
                else:
                    flash(err, "danger")
            return redirect(url_for("admin_configuracion"))

        try:
            roles = api.get("/v1/roles/")
            estatus = api.get("/v1/estatus-pedido/")
            parametros = api.get("/v1/parametros-sistema/")
            raw_u = api.get("/v1/usuarios/")
            usuarios_cfg = raw_u.get("usuarios", []) if isinstance(raw_u, dict) else []
            por_rol = defaultdict(int)
            for u in usuarios_cfg:
                por_rol[int(u.get("rol_id") or 0)] += 1
            for r in roles:
                r["_num_usuarios"] = por_rol.get(int(r["id"]), 0)
        except ApiError as e:
            flash(str(e.message), "danger")
            roles, estatus, parametros = [], [], []
        return render_template(
            "admin_configuracion.html",
            roles=roles,
            estatus_list=estatus,
            parametros=parametros,
        )

    @app.route("/admin/pedidos", methods=["GET"])
    def admin_pedidos():
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        try:
            pedidos = api.get("/v1/pedidos/admin/vista", params={"limit": 400})
            if not isinstance(pedidos, list):
                pedidos = []
            estatus_opts = api.get("/v1/estatus-pedido/")
        except ApiError as e:
            flash(str(e.message), "danger")
            pedidos, estatus_opts = [], []
        total = len(pedidos)
        pendientes = sum(1 for p in pedidos if p.get("estatus") == "Pendiente")
        en_proceso = sum(
            1
            for p in pedidos
            if p.get("estatus") in ("Surtiendo", "Empacado", "Enviado")
        )
        entregados = sum(1 for p in pedidos if p.get("estatus") == "Entregado")
        cancelados = sum(1 for p in pedidos if p.get("motivo_cancelacion"))
        kpi_pedidos = {
            "total": total,
            "pendientes": pendientes,
            "en_proceso": en_proceso,
            "entregados": entregados,
            "cancelados": cancelados,
        }
        return render_template(
            "admin_pedidos.html",
            pedidos=pedidos,
            estatus_opts=estatus_opts,
            kpi_pedidos=kpi_pedidos,
        )

    @app.route("/admin/contacto-portal", methods=["GET"])
    def admin_contacto_portal():
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        try:
            mensajes = api.get("/v1/portal-contacto/mensajes")
            if not isinstance(mensajes, list):
                mensajes = []
        except ApiError as e:
            flash(str(e.message), "danger")
            mensajes = []
        return render_template("admin_contacto_portal.html", mensajes=mensajes)

    @app.route("/admin/contacto-portal/<int:mid>/leido", methods=["POST"])
    def admin_contacto_portal_leido(mid):
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        try:
            api.patch(f"/v1/portal-contacto/mensajes/{mid}/leido", json={})
            flash("Mensaje marcado como leído.", "success")
        except ApiError as e:
            flash(str(e.message), "danger")
        return redirect(url_for("admin_contacto_portal"))

    @app.route("/admin/contacto-portal/<int:mid>/responder", methods=["POST"])
    def admin_contacto_portal_responder(mid):
        redir = solo_admin()
        if redir:
            return redir
        texto = (request.form.get("admin_reply") or "").strip()
        if not texto:
            flash("La respuesta no puede estar vacía.", "danger")
            return redirect(url_for("admin_contacto_portal"))
        api = get_api()
        try:
            api.patch(f"/v1/portal-contacto/mensajes/{mid}/responder", json={"admin_reply": texto})
            flash("Respuesta guardada y visible para el cliente en su cuenta.", "success")
        except ApiError as e:
            flash(str(e.message), "danger")
        return redirect(url_for("admin_contacto_portal"))

    @app.route("/admin/contacto-portal/<int:mid>/eliminar", methods=["POST"])
    def admin_contacto_portal_eliminar(mid):
        redir = solo_admin()
        if redir:
            return redir
        api = get_api()
        try:
            api.delete(f"/v1/portal-contacto/mensajes/{mid}")
            flash("Mensaje eliminado.", "success")
        except ApiError as e:
            flash(str(e.message), "danger")
        return redirect(url_for("admin_contacto_portal"))
