from flask import render_template, redirect, url_for, request, session, jsonify

def register_routes(app):

    # Base de datos simulada
    USUARIOS = {
        "admin": {
            "nombre": "Frank Contreras",
            "correo": "admin@macuin.com",
            "rol": "Administrador",
            "password": "admin123"
        },
        "ventas": {
            "nombre": "María González",
            "correo": "ventas@macuin.com",
            "rol": "Ventas",
            "password": "ventas123"
        },
        "logistica": {
            "nombre": "Ana Martínez",
            "correo": "logistica@macuin.com",
            "rol": "Logística",
            "password": "logistica123"
        },
        "almacen": {
            "nombre": "Carlos López",
            "correo": "almacen@macuin.com",
            "rol": "Almacén",
            "password": "almacen123"
        }
    }

    def requiere_login():
        return 'user_id' not in session

    def requiere_rol(rol):
        return session.get('user_role') != rol

    # -------- LOGIN --------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            perfil = request.form.get('perfil')
            correo = request.form.get('correo')
            password = request.form.get('password')

            print(f"LOGIN ATTEMPT: perfil='{perfil}', correo='{correo}', password='{password}'", flush=True)

            if perfil in USUARIOS:
                user = USUARIOS[perfil]
                if correo == user["correo"] and password == user["password"]:
                    session['user_id']    = perfil
                    session['user_name']  = user["nombre"]
                    session['user_email'] = user["correo"]
                    session['user_role']  = user["rol"]
                    print(f"LOGIN SUCCESS: {perfil}", flush=True)

                    # Redirige según rol
                    if user["rol"] == "Ventas":
                        return redirect(url_for('ventas_dashboard'))
                    if user["rol"] == "Logística":
                        return redirect(url_for('logistica_dashboard'))
                    if user["rol"] == "Almacén":
                        return redirect(url_for('almacen_dashboard'))
                    if user["rol"] == "Administrador":
                        return redirect(url_for('admin_dashboard'))
                    return redirect(url_for('index'))
                else:
                    print(f"LOGIN FAILED: expected {user['correo']} / {user['password']}", flush=True)
            else:
                print(f"LOGIN FAILED PERFIL NOT FOUND: '{perfil}'", flush=True)

        return render_template("login.html")

    # -------- LOGOUT --------
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    # -------- DASHBOARD GENERAL --------
    @app.route('/')
    @app.route('/dashboard')
    def index():
        if requiere_login():
            return redirect(url_for('login'))
        # Cada rol va a su propio dashboard
        if session.get('user_role') == 'Ventas':
            return redirect(url_for('ventas_dashboard'))
        if session.get('user_role') == 'Logística':
            return redirect(url_for('logistica_dashboard'))
        if session.get('user_role') == 'Almacén':
            return redirect(url_for('almacen_dashboard'))
        if session.get('user_role') == 'Administrador':
            return redirect(url_for('admin_dashboard'))
        return render_template('index.html')

    # -------- INVENTORY (SOLO ALMACEN) --------
    @app.route('/inventory')
    def inventory():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol("Almacén"):
            return redirect(url_for('index'))
        return render_template('inventory.html')

    # -------- USUARIOS INTERNOS (legacy - dejado para compatibilidad) --------
    @app.route('/users')
    def users():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol("Ventas"):
            return redirect(url_for('index'))
        return redirect(url_for('ventas_clientes'))

    # -------- ADMINISTRADOR (legacy redirect) --------
    @app.route('/administrador')
    def administrador():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Administrador'):
            return redirect(url_for('index'))
        return redirect(url_for('admin_dashboard'))

    # ==============================================================
    # MÓDULO ADMINISTRADOR
    # ==============================================================

    def solo_admin():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Administrador'):
            return redirect(url_for('index'))
        return None

    # -------- ADMIN DASHBOARD --------
    @app.route('/admin')
    @app.route('/admin/dashboard')
    def admin_dashboard():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_dashboard.html')

    # -------- ADMIN: USUARIOS INTERNOS (CRUD) --------
    @app.route('/admin/usuarios', methods=['GET'])
    def admin_usuarios():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_usuarios.html')

    @app.route('/admin/usuarios/nuevo', methods=['POST'])
    def admin_usuarios_nuevo():
        """Da de alta a un nuevo empleado."""
        redir = solo_admin()
        if redir:
            return redir
        nombre   = request.form.get('nombre', '').strip()
        correo   = request.form.get('correo', '').strip()
        rol      = request.form.get('rol', '').strip()
        password = request.form.get('password', '').strip()
        # → Aquí se conectará con el API de Laravel (POST /api/usuarios)
        return redirect(url_for('admin_usuarios'))

    @app.route('/admin/usuarios/<usuario_id>/editar', methods=['GET', 'POST'])
    def admin_usuarios_editar(usuario_id):
        """Edita nombre, correo o rol del empleado."""
        redir = solo_admin()
        if redir:
            return redir
        if request.method == 'POST':
            nombre = request.form.get('nombre', '').strip()
            correo = request.form.get('correo', '').strip()
            rol    = request.form.get('rol', '').strip()
            # → Aquí se conectará con el API de Laravel (PUT /api/usuarios/{id})
            return redirect(url_for('admin_usuarios'))
        return render_template('admin_usuarios.html')

    @app.route('/admin/usuarios/<usuario_id>/reset', methods=['POST'])
    def admin_usuarios_reset(usuario_id):
        """Resetea la contraseña del empleado."""
        redir = solo_admin()
        if redir:
            return redir
        nueva_password = request.form.get('password', '').strip()
        # → Aquí se conectará con el API de Laravel (PATCH /api/usuarios/{id}/reset)
        return redirect(url_for('admin_usuarios'))

    @app.route('/admin/usuarios/<usuario_id>/baja', methods=['POST'])
    def admin_usuarios_baja(usuario_id):
        """Soft delete: marca al usuario como Inactivo. Nunca elimina registros."""
        redir = solo_admin()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (PATCH /api/usuarios/{id}/baja)
        return redirect(url_for('admin_usuarios'))

    # -------- ADMIN: CATÁLOGO MAESTRO (CRUD) --------
    @app.route('/admin/catalogo', methods=['GET'])
    def admin_catalogo():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_catalogo.html')

    @app.route('/admin/catalogo/nuevo', methods=['POST'])
    def admin_catalogo_nuevo():
        """Crea una nueva autoparte en el catálogo maestro."""
        redir = solo_admin()
        if redir:
            return redir
        id       = request.form.get('id', '').strip()
        nombre    = request.form.get('nombre', '').strip()
        categoria = request.form.get('categoria', '').strip()
        marca     = request.form.get('marca', '').strip()
        precio    = request.form.get('precio', 0)
        # → Aquí se conectará con el API de Laravel (POST /api/autopartes)
        return redirect(url_for('admin_catalogo'))

    @app.route('/admin/catalogo/<autoparte_id>/editar', methods=['GET', 'POST'])
    def admin_catalogo_editar(autoparte_id):
        redir = solo_admin()
        if redir:
            return redir
        if request.method == 'POST':
            nombre    = request.form.get('nombre', '').strip()
            categoria = request.form.get('categoria', '').strip()
            marca     = request.form.get('marca', '').strip()
            precio    = request.form.get('precio', 0)
            # → Aquí se conectará con el API de Laravel (PUT /api/autopartes/{id})
            return redirect(url_for('admin_catalogo'))
        return render_template('admin_catalogo.html')

    @app.route('/admin/catalogo/<autoparte_id>/eliminar', methods=['POST'])
    def admin_catalogo_eliminar(autoparte_id):
        redir = solo_admin()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (DELETE /api/autopartes/{id})
        return redirect(url_for('admin_catalogo'))

    # -------- ADMIN: CONFIGURACIÓN (CRUD) --------
    @app.route('/admin/configuracion', methods=['GET'])
    def admin_configuracion():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_configuracion.html')

    @app.route('/admin/configuracion/nuevo', methods=['POST'])
    def admin_configuracion_nuevo():
        """Crea un nuevo rol, estatus o parámetro."""
        redir = solo_admin()
        if redir:
            return redir
        tipo  = request.form.get('tipo', '').strip()   # 'rol' | 'estatus' | 'parametro'
        clave = request.form.get('clave', '').strip()
        valor = request.form.get('valor', '').strip()
        # → Aquí se conectará con el API de Laravel
        return redirect(url_for('admin_configuracion'))

    @app.route('/admin/configuracion/<config_id>/editar', methods=['GET', 'POST'])
    def admin_configuracion_editar(config_id):
        redir = solo_admin()
        if redir:
            return redir
        if request.method == 'POST':
            clave = request.form.get('clave', '').strip()
            valor = request.form.get('valor', '').strip()
            # → Aquí se conectará con el API de Laravel (PUT /api/configuracion/{id})
            return redirect(url_for('admin_configuracion'))
        return render_template('admin_configuracion.html')

    @app.route('/admin/configuracion/<config_id>/eliminar', methods=['POST'])
    def admin_configuracion_eliminar(config_id):
        redir = solo_admin()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (DELETE /api/configuracion/{id})
        return redirect(url_for('admin_configuracion'))

    # -------- ADMIN: PEDIDOS (Solo lectura) --------
    @app.route('/admin/pedidos', methods=['GET'])
    def admin_pedidos():
        """Vista de solo lectura para todos los pedidos del sistema."""
        redir = solo_admin()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (GET /api/pedidos)
        return render_template('admin_pedidos.html')



    # -------- CATALOGO LOGISTICA --------
    @app.route('/catalog')
    def catalog():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol("Logística"):
            return redirect(url_for('index'))
        return render_template('catalog.html')

    # ==============================================================
    # MÓDULO VENTAS
    # ==============================================================

    def solo_ventas():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Ventas'):
            return redirect(url_for('index'))
        return None

    # -------- VENTAS DASHBOARD --------
    @app.route('/ventas')
    @app.route('/ventas/dashboard')
    def ventas_dashboard():
        redir = solo_ventas()
        if redir:
            return redir
        return render_template('ventas_dashboard.html')

    # -------- VENTAS: CLIENTES (CRUD externo) --------
    @app.route('/ventas/clientes', methods=['GET', 'POST'])
    def ventas_clientes():
        redir = solo_ventas()
        if redir:
            return redir
        if request.method == 'POST':
            nombre   = request.form.get('nombre', '').strip()
            correo   = request.form.get('correo', '').strip()
            telefono = request.form.get('telefono', '').strip()
            # → Aquí se conectará con el API de Laravel para persistir
            return redirect(url_for('ventas_clientes'))
        return render_template('ventas_clientes.html')

    @app.route('/ventas/clientes/<cliente_id>/editar', methods=['GET', 'POST'])
    def ventas_clientes_editar(cliente_id):
        redir = solo_ventas()
        if redir:
            return redir
        if request.method == 'POST':
            nuevo_correo = request.form.get('correo', '').strip()
            # → Aquí se conectará con el API de Laravel (PUT /api/clientes/{id})
            return redirect(url_for('ventas_clientes'))
        return render_template('ventas_clientes.html')

    @app.route('/ventas/clientes/<cliente_id>/baja', methods=['POST'])
    def ventas_clientes_baja(cliente_id):
        """Soft delete: marca al cliente como Inactivo. Nunca elimina registros."""
        redir = solo_ventas()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (PATCH /api/clientes/{id}/baja)
        return redirect(url_for('ventas_clientes'))

    # -------- VENTAS: PEDIDOS (CRU — sin Delete) --------
    @app.route('/ventas/pedidos', methods=['GET'])
    def ventas_pedidos():
        redir = solo_ventas()
        if redir:
            return redir
        return render_template('ventas_pedidos.html')

    @app.route('/ventas/pedidos/nuevo', methods=['GET', 'POST'])
    def ventas_pedido_nuevo():
        redir = solo_ventas()
        if redir:
            return redir
        if request.method == 'POST':
            cliente_id = request.form.get('cliente_id')
            direccion  = request.form.get('direccion', '').strip()
            piezas     = request.form.getlist('pieza_codigo')
            cantidades = request.form.getlist('pieza_cantidad')
            # → Aquí se conectará con el API de Laravel (POST /api/pedidos)
            return redirect(url_for('ventas_pedidos'))
        return render_template('ventas_pedidos.html')

    @app.route('/ventas/pedidos/<pedido_id>/editar', methods=['GET', 'POST'])
    def ventas_pedido_editar(pedido_id):
        """Permite actualizar dirección o CANCELAR. NUNCA borrar."""
        redir = solo_ventas()
        if redir:
            return redir
        if request.method == 'POST':
            accion    = request.form.get('accion')          # 'direccion' | 'cancelar'
            direccion = request.form.get('direccion', '').strip()
            motivo    = request.form.get('motivo', '').strip()
            # → Aquí se conectará con el API de Laravel (PATCH /api/pedidos/{id})
            return redirect(url_for('ventas_pedidos'))
        return render_template('ventas_pedidos.html')

    # -------- VENTAS: CATÁLOGO (Solo lectura) --------
    @app.route('/ventas/catalogo')
    def ventas_catalogo():
        redir = solo_ventas()
        if redir:
            return redir
        # → Aquí se puede conectar con el API de Laravel (GET /api/productos)
        return render_template('ventas_catalogo.html')

    # ==============================================================
    # MÓDULO LOGÍSTICA
    # ==============================================================

    def solo_logistica():
        """Helper: devuelve redirect si el usuario NO es Logística."""
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Logística'):
            return redirect(url_for('index'))
        return None

    # -------- LOGÍSTICA DASHBOARD --------
    @app.route('/logistica')
    @app.route('/logistica/dashboard')
    def logistica_dashboard():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_dashboard.html')

    # -------- LOGÍSTICA: ENVÍOS (R U — solo estatus ENVIADO / ENTREGADO) --------
    @app.route('/logistica/envios', methods=['GET'])
    def logistica_envios():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_envios.html')

    @app.route('/logistica/envios/<pedido_id>/estatus', methods=['POST'])
    def logistica_envios_estatus(pedido_id):
        """Solo permite actualizar estatus a ENVIADO o ENTREGADO."""
        redir = solo_logistica()
        if redir:
            return redir
        nuevo_estatus = request.form.get('estatus', '').strip()
        # Validación: únicamente los dos estatus permitidos
        if nuevo_estatus not in ('Enviado', 'Entregado'):
            return redirect(url_for('logistica_envios'))
        # → Aquí se conectará con el API de Laravel (PATCH /api/pedidos/{id}/estatus)
        return redirect(url_for('logistica_envios'))

    # -------- LOGÍSTICA: DIRECCIONES (R — solo lectura) --------
    @app.route('/logistica/direcciones')
    def logistica_direcciones():
        redir = solo_logistica()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (GET /api/pedidos/{id}/direccion)
        return render_template('logistica_direcciones.html')

    # -------- LOGÍSTICA: GUÍAS (CRUD completo) --------
    @app.route('/logistica/guias', methods=['GET'])
    def logistica_guias():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_guias.html')

    @app.route('/logistica/guias/nueva', methods=['POST'])
    def logistica_guias_nueva():
        """Sube un PDF o genera etiqueta de ruta."""
        redir = solo_logistica()
        if redir:
            return redir
        pedido_id   = request.form.get('pedido_id')
        paqueteria  = request.form.get('paqueteria', '').strip()
        rastreo     = request.form.get('rastreo', '').strip()
        tipo        = request.form.get('tipo', 'PDF')   # 'PDF' | 'Etiqueta'
        # archivo = request.files.get('pdf_file')       # para manejo de archivo
        # → Aquí se conectará con el API de Laravel (POST /api/guias)
        return redirect(url_for('logistica_guias'))

    @app.route('/logistica/guias/<guia_id>/editar', methods=['GET', 'POST'])
    def logistica_guias_editar(guia_id):
        redir = solo_logistica()
        if redir:
            return redir
        if request.method == 'POST':
            paqueteria = request.form.get('paqueteria', '').strip()
            rastreo    = request.form.get('rastreo', '').strip()
            # → Aquí se conectará con el API de Laravel (PUT /api/guias/{id})
            return redirect(url_for('logistica_guias'))
        return render_template('logistica_guias.html')

    @app.route('/logistica/guias/<guia_id>/eliminar', methods=['POST'])
    def logistica_guias_eliminar(guia_id):
        """Elimina el documento de envío (NO el pedido)."""
        redir = solo_logistica()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (DELETE /api/guias/{id})
        return redirect(url_for('logistica_guias'))

    # ==============================================================
    # MÓDULO ALMACÉN
    # ==============================================================

    def solo_almacen():
        """Helper: devuelve redirect si el usuario NO es Almacén."""
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Almacén'):
            return redirect(url_for('index'))
        return None

    # -------- ALMACÉN DASHBOARD --------
    @app.route('/almacen')
    @app.route('/almacen/dashboard')
    def almacen_dashboard():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_dashboard.html')

    # -------- ALMACÉN: INVENTARIO (CRU — ajuste de stock y mermas) --------
    @app.route('/almacen/inventario', methods=['GET'])
    def almacen_inventario():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_inventario.html')

    @app.route('/almacen/inventario/ajustar', methods=['POST'])
    def almacen_inventario_ajustar():
        """Suma stock (entrada) o resta Stock (merma). Nunca elimina el ID."""
        redir = solo_almacen()
        if redir:
            return redir
        id       = request.form.get('id', '').strip()
        tipo      = request.form.get('tipo', '').strip()   # 'entrada' | 'merma'
        cantidad  = request.form.get('cantidad', 0)
        # → Aquí se conectará con el API de Laravel (POST /api/inventario/ajustar)
        return redirect(url_for('almacen_inventario'))

    # -------- ALMACÉN: UBICACIONES (CRUD) --------
    @app.route('/almacen/ubicaciones', methods=['GET'])
    def almacen_ubicaciones():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_ubicaciones.html')

    @app.route('/almacen/ubicaciones/nueva', methods=['POST'])
    def almacen_ubicaciones_nueva():
        redir = solo_almacen()
        if redir:
            return redir
        pasillo     = request.form.get('pasillo', '').strip()
        estante     = request.form.get('estante', '').strip()
        capacidad   = request.form.get('capacidad', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        # → Aquí se conectará con el API de Laravel (POST /api/ubicaciones)
        return redirect(url_for('almacen_ubicaciones'))

    @app.route('/almacen/ubicaciones/<ubicacion_id>/editar', methods=['GET', 'POST'])
    def almacen_ubicaciones_editar(ubicacion_id):
        redir = solo_almacen()
        if redir:
            return redir
        if request.method == 'POST':
            capacidad   = request.form.get('capacidad', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            # → Aquí se conectará con el API de Laravel (PUT /api/ubicaciones/{id})
            return redirect(url_for('almacen_ubicaciones'))
        return render_template('almacen_ubicaciones.html')

    @app.route('/almacen/ubicaciones/<ubicacion_id>/eliminar', methods=['POST'])
    def almacen_ubicaciones_eliminar(ubicacion_id):
        """Solo permite si no hay stock asignado a esa ubicación."""
        redir = solo_almacen()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (DELETE /api/ubicaciones/{id})
        return redirect(url_for('almacen_ubicaciones'))

    # -------- ALMACÉN: PEDIDOS (R U — solo estatus SURTIENDO / EMPACADO) --------
    @app.route('/almacen/pedidos', methods=['GET'])
    def almacen_pedidos():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_pedidos.html')

    @app.route('/almacen/pedidos/<pedido_id>/estatus', methods=['POST'])
    def almacen_pedidos_estatus(pedido_id):
        """Solo permite actualizar estatus a SURTIENDO o EMPACADO."""
        redir = solo_almacen()
        if redir:
            return redir
        nuevo_estatus = request.form.get('estatus', '').strip()
        if nuevo_estatus not in ('Surtiendo', 'Empacado'):
            return redirect(url_for('almacen_pedidos'))
        # → Aquí se conectará con el API de Laravel (PATCH /api/pedidos/{id}/estatus)
        return redirect(url_for('almacen_pedidos'))

    # -------- ALMACÉN: AUTOPARTES (Solo lectura) --------
    @app.route('/almacen/autopartes')
    def almacen_autopartes():
        redir = solo_almacen()
        if redir:
            return redir
        # → Aquí se conectará con el API de Laravel (GET /api/autopartes)
        return render_template('almacen_autopartes.html')