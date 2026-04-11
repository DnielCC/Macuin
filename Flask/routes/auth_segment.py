import requests
from flask import flash, redirect, render_template, request, session, url_for

from services.api import ApiError, get_api
from services.validators import validate_email, validate_password_plain


def _api_base_hint() -> str:
    api = get_api()
    return getattr(api, "base", "") or "(URL no configurada)"


def _short_msg(text: str, max_len: int = 480) -> str:
    t = (text or "").strip()
    if len(t) <= max_len:
        return t
    return t[: max_len - 1] + "…"


def register(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            ok, email = validate_email(request.form.get("correo"))
            if not ok:
                flash(email, "danger")
                return render_template("login.html")
            ok, pw = validate_password_plain(request.form.get("password"), min_len=6)
            if not ok:
                flash(pw, "danger")
                return render_template("login.html")
            api = get_api()
            try:
                data = api.post_public(
                    "/v1/auth/login",
                    json={"email": email, "password": pw},
                )
            except ApiError as e:
                base = _api_base_hint()
                detail = _short_msg(str(e.message))
                if e.status_code == 401:
                    flash(
                        f"Inicio de sesión rechazado: {detail}. "
                        f"Si acabas de instalar el proyecto, ejecuta en el contenedor API: "
                        f"python scripts/seed_macuin_demo_users.py (ver README-CREDENCIALES.md). "
                        f"API: {base}",
                        "danger",
                    )
                elif e.status_code == 422:
                    flash(f"Datos no válidos para la API: {detail}", "danger")
                else:
                    flash(f"Error de la API ({e.status_code}): {detail}. Comprueba que la API esté en marcha. URL: {base}", "danger")
                return render_template("login.html")
            except requests.exceptions.RequestException as e:
                base = _api_base_hint()
                flash(
                    f"No hay conexión con la API ({base}). "
                    f"Detalle: {type(e).__name__}: {_short_msg(str(e), 200)}. "
                    f"¿Está levantado el servicio FastAPI (puerto 8000 o macuin_api en Docker)?",
                    "danger",
                )
                return render_template("login.html")
            except Exception as e:
                app.logger.exception("Error en login Flask")
                flash(f"Error inesperado al iniciar sesión: {_short_msg(str(e), 200)}", "danger")
                return render_template("login.html")
            session["user_id"] = data["id"]
            session["user_name"] = f"{data['nombre']} {data['apellidos']}".strip()
            session["user_email"] = data["email"]
            session["user_role"] = data["rol"]
            flash(f"Sesión iniciada como {data['rol']}.", "success")
            r = data["rol"]
            if r == "Ventas":
                return redirect(url_for("ventas_dashboard"))
            if r == "Logística":
                return redirect(url_for("logistica_dashboard"))
            if r == "Almacén":
                return redirect(url_for("almacen_dashboard"))
            if r == "Administrador":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("index"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Sesión cerrada correctamente.", "info")
        return redirect(url_for("login"))
