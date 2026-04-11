from flask import redirect, render_template, session, url_for


def register(app):
    def requiere_login():
        return "user_id" not in session

    def requiere_rol(rol):
        return session.get("user_role") != rol

    @app.route("/")
    @app.route("/dashboard")
    def index():
        if requiere_login():
            return redirect(url_for("login"))
        r = session.get("user_role")
        if r == "Ventas":
            return redirect(url_for("ventas_dashboard"))
        if r == "Logística":
            return redirect(url_for("logistica_dashboard"))
        if r == "Almacén":
            return redirect(url_for("almacen_dashboard"))
        if r == "Administrador":
            return redirect(url_for("admin_dashboard"))
        return render_template("index.html")

    @app.route("/inventory")
    def inventory():
        if requiere_login():
            return redirect(url_for("login"))
        if requiere_rol("Almacén"):
            return redirect(url_for("index"))
        return render_template("inventory.html")

    @app.route("/users")
    def users():
        if requiere_login():
            return redirect(url_for("login"))
        if requiere_rol("Ventas"):
            return redirect(url_for("index"))
        return redirect(url_for("ventas_clientes"))

    @app.route("/administrador")
    def administrador():
        if requiere_login():
            return redirect(url_for("login"))
        if requiere_rol("Administrador"):
            return redirect(url_for("index"))
        return redirect(url_for("admin_dashboard"))

    @app.route("/catalog")
    def catalog():
        if requiere_login():
            return redirect(url_for("login"))
        if requiere_rol("Logística"):
            return redirect(url_for("index"))
        return render_template("catalog.html")
