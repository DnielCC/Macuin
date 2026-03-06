from flask import render_template, redirect, url_for, request, session

def register_routes(app):

    # Base de datos simulada
    USUARIOS = {
        "ventas": {
            "nombre": "María González",
            "correo": "ventas@macuin.com",
            "rol": "Ventas",
            "password": "1234"
        },
        "logistica": {
            "nombre": "Ana Martínez",
            "correo": "logistica@macuin.com",
            "rol": "Logística",
            "password": "1234"
        },
        "almacen": {
            "nombre": "Carlos López",
            "correo": "almacen@macuin.com",
            "rol": "Almacén",
            "password": "1234"
        }
    }

    # -------- LOGIN --------
    @app.route('/login', methods=['GET','POST'])
    def login():

        if request.method == 'POST':

            perfil = request.form.get('perfil')
            correo = request.form.get('correo')
            password = request.form.get('password')

            if perfil in USUARIOS:

                user = USUARIOS[perfil]

                if correo == user["correo"] and password == user["password"]:

                    session['user_id'] = perfil
                    session['user_name'] = user["nombre"]
                    session['user_email'] = user["correo"]
                    session['user_role'] = user["rol"]

                    return redirect(url_for('index'))

        return render_template("login.html")


    # -------- LOGOUT --------
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))


    # -------- DASHBOARD --------
    @app.route('/')
    @app.route('/dashboard')
    def index():

        if 'user_id' not in session:
            return redirect(url_for('login'))

        return render_template('index.html')


    # -------- INVENTORY (SOLO ALMACEN) --------
    @app.route('/inventory')
    def inventory():

        if 'user_id' not in session:
            return redirect(url_for('login'))

        if session.get("user_role") != "Almacén":
            return redirect(url_for('index'))

        return render_template('inventory.html')

# -------- USUARIOS (VENTAS) --------
    @app.route('/users')
    def users():
        # 1. Primero revisamos si está logueado
        if 'user_id' not in session:
            return redirect(url_for('login'))

        # 2. AHORA SÍ: Revisamos el rol dentro de la función (Correctamente indentado)
        if session.get("user_role") != "Ventas":
            return redirect(url_for('index'))

        # 3. Definimos la lista y renderizamos (Todo esto va dentro de users)
        lista_usuarios = [
            {"nombre":"María González","email":"ventas@macuin.com","departamento":"Ventas","estado":"Activo"},
            {"nombre":"Ana Martínez","email":"logistica@macuin.com","departamento":"Logística","estado":"Activo"},
            {"nombre":"Carlos López","email":"almacen@macuin.com","departamento":"Almacén","estado":"Activo"}
        ]

        return render_template('users.html', usuarios=lista_usuarios)

    # -------- CATALOGO (LOGISTICA) --------
    @app.route('/catalog')
    def catalog():

        if 'user_id' not in session:
            return redirect(url_for('login'))

        if session.get("user_role") != "Logística":
            return redirect(url_for('index'))

        return render_template('catalog.html')


   # -------- VISTA PROYECTO --------
    @app.route('/vista_proyecto')
    def vista_proyecto():  # <--- AQUÍ: Cambia "index" por "vista_proyecto"
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
    # Tu lógica aquí...
        return render_template('vista_proyecto.html')
