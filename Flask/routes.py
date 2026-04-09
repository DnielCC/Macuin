from flask import render_template, redirect, url_for, request, session, jsonify
import requests
import os
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
API_USER = os.getenv("API_USER", "alidaniel")
API_PASS = os.getenv("API_PASS", "123456")
API_AUTH = (API_USER, API_PASS)
def api_get(path, params=None):
    """GET sin autenticación (endpoints públicos de lectura)."""
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.RequestException as e:
        return None, str(e)
def api_get_auth(path, params=None):
    """GET con autenticación básica."""
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, auth=API_AUTH, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.RequestException as e:
        return None, str(e)
def api_post(path, data):
    try:
        r = requests.post(f"{API_BASE}{path}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.RequestException as e:
        return None, str(e)
def api_put(path, data):
    try:
        r = requests.put(f"{API_BASE}{path}", json=data, auth=API_AUTH, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.RequestException as e:
        return None, str(e)
def api_delete(path):
    try:
        r = requests.delete(f"{API_BASE}{path}", auth=API_AUTH, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.RequestException as e:
        return None, str(e)
def register_routes(app):
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
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))
    @app.route('/')
    @app.route('/dashboard')
    def index():
        if requiere_login():
            return redirect(url_for('login'))
        if session.get('user_role') == 'Ventas':
            return redirect(url_for('ventas_dashboard'))
        if session.get('user_role') == 'Logística':
            return redirect(url_for('logistica_dashboard'))
        if session.get('user_role') == 'Almacén':
            return redirect(url_for('almacen_dashboard'))
        if session.get('user_role') == 'Administrador':
            return redirect(url_for('admin_dashboard'))
        return render_template('index.html')
    
    @app.route('/inventory')
    def inventory():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol("Almacén"):
            return redirect(url_for('index'))
        return render_template('inventory.html')
    @app.route('/users')
    def users():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol("Ventas"):
            return redirect(url_for('index'))
        return redirect(url_for('ventas_clientes'))
    @app.route('/administrador')
    def administrador():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Administrador'):
            return redirect(url_for('index'))
        return redirect(url_for('admin_dashboard'))
    def solo_admin():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Administrador'):
            return redirect(url_for('index'))
        return None
    @app.route('/admin')
    @app.route('/admin/dashboard')
    def admin_dashboard():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_dashboard.html')
    @app.route('/admin/usuarios', methods=['GET'])
    def admin_usuarios():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_usuarios.html')
    @app.route('/admin/usuarios/nuevo', methods=['POST'])
    def admin_usuarios_nuevo():
        redir = solo_admin()
        if redir:
            return redir
        data = {
            "nombre":       request.form.get('nombre', '').strip(),
            "apellidos":    request.form.get('apellidos', '').strip(),
            "email":        request.form.get('correo', '').strip(),
            "password_hash": request.form.get('password', '').strip(),
            "telefono":     request.form.get('telefono', '').strip() or None,
            "rol_id":       int(request.form.get('rol_id', 1)),
            "activo":       True,
        }
        api_post("/v1/usuarios/", data)
        return redirect(url_for('admin_usuarios'))
    @app.route('/admin/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
    def admin_usuarios_editar(usuario_id):
        redir = solo_admin()
        if redir:
            return redir
        if request.method == 'POST':
            data = {
                "nombre": request.form.get('nombre', '').strip(),
                "apellidos": request.form.get('apellidos', '').strip(),
                "email": request.form.get('correo', '').strip(),
                "password_hash": request.form.get('password', '').strip(),
                "rol_id": int(request.form.get('rol_id', 1)),
                "activo": True,
            }
            api_put(f"/v1/usuarios/{usuario_id}", data)
            return redirect(url_for('admin_usuarios'))
        return render_template('admin_usuarios.html')
    @app.route('/admin/usuarios/<int:usuario_id>/baja', methods=['POST'])
    def admin_usuarios_baja(usuario_id):
        redir = solo_admin()
        if redir:
            return redir
        usuario, _ = api_get(f"/v1/usuarios/{usuario_id}")
        if usuario:
            usuario['activo'] = False
            api_put(f"/v1/usuarios/{usuario_id}", usuario)
        return redirect(url_for('admin_usuarios'))
    @app.route('/admin/catalogo', methods=['GET'])
    def admin_catalogo():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_catalogo.html')
    @app.route('/admin/catalogo/nuevo', methods=['POST'])
    def admin_catalogo_nuevo():
        redir = solo_admin()
        if redir:
            return redir
        data = {
            "sku_codigo":      request.form.get('id', '').strip(),
            "nombre":          request.form.get('nombre', '').strip(),
            "categoria_id":    int(request.form.get('categoria_id', 1)),
            "marca_id":        int(request.form.get('marca_id', 1)),
            "precio_unitario": float(request.form.get('precio', 0)),
        }
        api_post("/v1/autopartes/", data)
        return redirect(url_for('admin_catalogo'))
    @app.route('/admin/catalogo/<int:autoparte_id>/editar', methods=['GET', 'POST'])
    def admin_catalogo_editar(autoparte_id):
        redir = solo_admin()
        if redir:
            return redir
        if request.method == 'POST':
            data = {
                "nombre": request.form.get('nombre', '').strip(),
                "categoria_id": int(request.form.get('categoria_id', 1)),
                "marca_id": int(request.form.get('marca_id', 1)),
                "precio_unitario":float(request.form.get('precio', 0)),
            }
            api_put(f"/v1/autopartes/{autoparte_id}", data)
            return redirect(url_for('admin_catalogo'))
        return render_template('admin_catalogo.html')
    @app.route('/admin/catalogo/<int:autoparte_id>/eliminar', methods=['POST'])
    def admin_catalogo_eliminar(autoparte_id):
        redir = solo_admin()
        if redir:
            return redir
        api_delete(f"/v1/autopartes/{autoparte_id}")
        return redirect(url_for('admin_catalogo'))
    @app.route('/admin/configuracion', methods=['GET'])
    def admin_configuracion():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_configuracion.html')
    @app.route('/admin/configuracion/nuevo', methods=['POST'])
    def admin_configuracion_nuevo():
        redir = solo_admin()
        if redir:
            return redir
        tipo  = request.form.get('tipo', '').strip()
        valor = request.form.get('valor', '').strip()
        if tipo == 'rol':
            api_post("/v1/roles/", {"nombre_rol": valor})
        elif tipo == 'estatus':
            api_post("/v1/estatus_pedido/", {"nombre": valor})
        return redirect(url_for('admin_configuracion'))
    @app.route('/admin/configuracion/<int:config_id>/editar', methods=['GET', 'POST'])
    def admin_configuracion_editar(config_id):
        redir = solo_admin()
        if redir:
            return redir
        if request.method == 'POST':
            tipo  = request.form.get('tipo', '').strip()
            valor = request.form.get('valor', '').strip()
            if tipo == 'rol':
                api_put(f"/v1/roles/{config_id}", {"nombre_rol": valor})
            return redirect(url_for('admin_configuracion'))
        return render_template('admin_configuracion.html')
    @app.route('/admin/configuracion/<int:config_id>/eliminar', methods=['POST'])
    def admin_configuracion_eliminar(config_id):
        redir = solo_admin()
        if redir:
            return redir
        tipo = request.form.get('tipo', '').strip()
        if tipo == 'rol':
            api_delete(f"/v1/roles/{config_id}")
        return redirect(url_for('admin_configuracion'))
    @app.route('/admin/pedidos', methods=['GET'])
    def admin_pedidos():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_pedidos.html')
    @app.route('/admin/reportes', methods=['GET'])
    def admin_reportes():
        redir = solo_admin()
        if redir:
            return redir
        return render_template('admin_reportes.html')
    @app.route('/catalog')
    def catalog():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol("Logística"):
            return redirect(url_for('index'))
        return render_template('catalog.html')
    def solo_ventas():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Ventas'):
            return redirect(url_for('index'))
        return None
    @app.route('/ventas')
    @app.route('/ventas/dashboard')
    def ventas_dashboard():
        redir = solo_ventas()
        if redir:
            return redir
        return render_template('ventas_dashboard.html')
    @app.route('/ventas/clientes', methods=['GET', 'POST'])
    def ventas_clientes():
        redir = solo_ventas()
        if redir:
            return redir
        if request.method == 'POST':
            data = {
                "nombre": request.form.get('nombre', '').strip(),
                "apellidos": request.form.get('apellidos', '').strip(),
                "email": request.form.get('correo', '').strip(),
                "telefono": request.form.get('telefono', '').strip() or None,
                "password_hash": "temporal",
                "rol_id": 3,
                "activo": True,
            }
            api_post("/v1/usuarios/", data)
            return redirect(url_for('ventas_clientes'))
        return render_template('ventas_clientes.html')
    @app.route('/ventas/clientes/<int:cliente_id>/editar', methods=['GET', 'POST'])
    def ventas_clientes_editar(cliente_id):
        redir = solo_ventas()
        if redir:
            return redir
        if request.method == 'POST':
            cliente, _ = api_get(f"/v1/usuarios/{cliente_id}")
            if cliente:
                cliente['email'] = request.form.get('correo', '').strip()
                api_put(f"/v1/usuarios/{cliente_id}", cliente)
            return redirect(url_for('ventas_clientes'))
        return render_template('ventas_clientes.html')
    @app.route('/ventas/clientes/<int:cliente_id>/baja', methods=['POST'])
    def ventas_clientes_baja(cliente_id):
        redir = solo_ventas()
        if redir:
            return redir
        cliente, _ = api_get(f"/v1/usuarios/{cliente_id}")
        if cliente:
            cliente['activo'] = False
            api_put(f"/v1/usuarios/{cliente_id}", cliente)
        return redirect(url_for('ventas_clientes'))
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
            data = {
                "usuario_id": int(request.form.get('cliente_id', 1)),
                "estatus_id": 1,
                "total": 0.00,
                "direccion_envio_id": int(request.form.get('direccion_id', 1)),
            }
            api_post("/v1/pedidos/", data)
            return redirect(url_for('ventas_pedidos'))
        return render_template('ventas_pedidos.html')
    @app.route('/ventas/pedidos/<int:pedido_id>/editar', methods=['GET', 'POST'])
    def ventas_pedido_editar(pedido_id):
        redir = solo_ventas()
        if redir:
            return redir
        if request.method == 'POST':
            pedido, _ = api_get(f"/v1/pedidos/{pedido_id}")
            if pedido:
                accion = request.form.get('accion')
                if accion == 'cancelar':
                    pedido['estatus_id'] = int(request.form.get('estatus_cancelado_id', pedido['estatus_id']))
                elif accion == 'direccion':
                    pedido['direccion_envio_id'] = int(request.form.get('direccion_id', pedido['direccion_envio_id']))
                api_put(f"/v1/pedidos/{pedido_id}", pedido)
            return redirect(url_for('ventas_pedidos'))
        return render_template('ventas_pedidos.html')
    @app.route('/ventas/catalogo')
    def ventas_catalogo():
        redir = solo_ventas()
        if redir:
            return redir
        return render_template('ventas_catalogo.html')
    @app.route('/ventas/reportes', methods=['GET'])
    def ventas_reportes():
        redir = solo_ventas()
        if redir:
            return redir
        return render_template('ventas_reportes.html')
    def solo_logistica():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Logística'):
            return redirect(url_for('index'))
        return None
    @app.route('/logistica')
    @app.route('/logistica/dashboard')
    def logistica_dashboard():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_dashboard.html')
    @app.route('/logistica/envios', methods=['GET'])
    def logistica_envios():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_envios.html')
    @app.route('/logistica/envios/<int:pedido_id>/estatus', methods=['POST'])
    def logistica_envios_estatus(pedido_id):
        redir = solo_logistica()
        if redir:
            return redir
        nuevo_estatus = request.form.get('estatus', '').strip()
        if nuevo_estatus not in ('Enviado', 'Entregado'):
            return redirect(url_for('logistica_envios'))
        pedido, _ = api_get(f"/v1/pedidos/{pedido_id}")
        if pedido:
            pedido['estatus_id'] = int(request.form.get('estatus_id', pedido['estatus_id']))
            api_put(f"/v1/pedidos/{pedido_id}", pedido)
        return redirect(url_for('logistica_envios'))
    @app.route('/logistica/direcciones')
    def logistica_direcciones():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_direcciones.html')
    @app.route('/logistica/guias', methods=['GET'])
    def logistica_guias():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_guias.html')
    @app.route('/logistica/guias/nueva', methods=['POST'])
    def logistica_guias_nueva():
        redir = solo_logistica()
        if redir:
            return redir
        return redirect(url_for('logistica_guias'))
    @app.route('/logistica/guias/<guia_id>/editar', methods=['GET', 'POST'])
    def logistica_guias_editar(guia_id):
        redir = solo_logistica()
        if redir:
            return redir
        if request.method == 'POST':
            return redirect(url_for('logistica_guias'))
        return render_template('logistica_guias.html')
    @app.route('/logistica/guias/<guia_id>/eliminar', methods=['POST'])
    def logistica_guias_eliminar(guia_id):
        redir = solo_logistica()
        if redir:
            return redir
        return redirect(url_for('logistica_guias'))
    @app.route('/logistica/reportes', methods=['GET'])
    def logistica_reportes():
        redir = solo_logistica()
        if redir:
            return redir
        return render_template('logistica_reportes.html')
    def solo_almacen():
        if requiere_login():
            return redirect(url_for('login'))
        if requiere_rol('Almacén'):
            return redirect(url_for('index'))
        return None
    @app.route('/almacen')
    @app.route('/almacen/dashboard')
    def almacen_dashboard():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_dashboard.html')
    @app.route('/almacen/inventario', methods=['GET'])
    def almacen_inventario():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_inventario.html')
    @app.route('/almacen/inventario/ajustar', methods=['POST'])
    def almacen_inventario_ajustar():
        redir = solo_almacen()
        if redir:
            return redir
        inventario_id = int(request.form.get('id', 0))
        tipo = request.form.get('tipo', '').strip()  
        cantidad = int(request.form.get('cantidad', 0))
        inv, _ = api_get(f"/v1/inventarios/{inventario_id}")
        if inv and cantidad > 0:
            if tipo == 'entrada':
                inv['stock_actual'] += cantidad
            elif tipo == 'merma':
                inv['stock_actual'] = max(0, inv['stock_actual'] - cantidad)
            api_put(f"/v1/inventarios/{inventario_id}", inv)
        return redirect(url_for('almacen_inventario'))
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
        inventario_id = int(request.form.get('inventario_id', 0))
        inv, _ = api_get(f"/v1/inventarios/{inventario_id}")
        if inv:
            inv['pasillo'] = request.form.get('pasillo', '').strip() or None
            inv['estante'] = request.form.get('estante', '').strip() or None
            inv['nivel']   = request.form.get('nivel', '').strip() or None
            api_put(f"/v1/inventarios/{inventario_id}", inv)
        return redirect(url_for('almacen_ubicaciones'))
    @app.route('/almacen/ubicaciones/<int:ubicacion_id>/editar', methods=['GET', 'POST'])
    def almacen_ubicaciones_editar(ubicacion_id):
        redir = solo_almacen()
        if redir:
            return redir
        if request.method == 'POST':
            inv, _ = api_get(f"/v1/inventarios/{ubicacion_id}")
            if inv:
                inv['pasillo'] = request.form.get('pasillo', inv.get('pasillo', '')).strip() or None
                inv['estante'] = request.form.get('estante', inv.get('estante', '')).strip() or None
                inv['nivel']   = request.form.get('nivel',   inv.get('nivel', '')).strip() or None
                api_put(f"/v1/inventarios/{ubicacion_id}", inv)
            return redirect(url_for('almacen_ubicaciones'))
        return render_template('almacen_ubicaciones.html')
    @app.route('/almacen/ubicaciones/<int:ubicacion_id>/eliminar', methods=['POST'])
    def almacen_ubicaciones_eliminar(ubicacion_id):
        redir = solo_almacen()
        if redir:
            return redir
        api_delete(f"/v1/inventarios/{ubicacion_id}")
        return redirect(url_for('almacen_ubicaciones'))
    @app.route('/almacen/pedidos', methods=['GET'])
    def almacen_pedidos():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_pedidos.html')
    @app.route('/almacen/pedidos/<int:pedido_id>/estatus', methods=['POST'])
    def almacen_pedidos_estatus(pedido_id):
        redir = solo_almacen()
        if redir:
            return redir
        nuevo_estatus = request.form.get('estatus', '').strip()
        if nuevo_estatus not in ('Surtiendo', 'Empacado'):
            return redirect(url_for('almacen_pedidos'))
        pedido, _ = api_get(f"/v1/pedidos/{pedido_id}")
        if pedido:
            pedido['estatus_id'] = int(request.form.get('estatus_id', pedido['estatus_id']))
            api_put(f"/v1/pedidos/{pedido_id}", pedido)
        return redirect(url_for('almacen_pedidos'))
    @app.route('/almacen/autopartes')
    def almacen_autopartes():
        redir = solo_almacen()
        if redir:
            return redir
        return render_template('almacen_autopartes.html')
    def _check_session():
        if 'user_id' not in session:
            return jsonify({"error": "No autenticado"}), 401
        return None

    # ── API PROXIES ──────────────────────────────────────────────────────────

    @app.route('/api/autopartes', methods=['GET'])
    def proxy_autopartes():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/autopartes/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/autopartes', methods=['POST'])
    def proxy_autopartes_post():
        err = _check_session()
        if err:
            return err
        data, error = api_post("/v1/autopartes/", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/autopartes/buscar', methods=['GET'])
    def proxy_autopartes_buscar():
        err = _check_session()
        if err:
            return err
        nombre = request.args.get('nombre', '')
        data, error = api_get("/v1/autopartes/buscar/", params={"nombre": nombre})
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/autopartes/<int:auto_id>', methods=['PUT'])
    def proxy_autopartes_put(auto_id):
        err = _check_session()
        if err:
            return err
        data, error = api_put(f"/v1/autopartes/{auto_id}", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/autopartes/<int:auto_id>', methods=['DELETE'])
    def proxy_autopartes_delete(auto_id):
        err = _check_session()
        if err:
            return err
        data, error = api_delete(f"/v1/autopartes/{auto_id}")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/inventarios', methods=['GET'])
    def proxy_inventarios():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/inventarios/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/inventarios/<int:inv_id>', methods=['GET'])
    def proxy_inventario_get(inv_id):
        err = _check_session()
        if err:
            return err
        data, error = api_get(f"/v1/inventarios/{inv_id}")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/inventarios/<int:inv_id>', methods=['PUT'])
    def proxy_inventario_put(inv_id):
        err = _check_session()
        if err:
            return err
        data, error = api_put(f"/v1/inventarios/{inv_id}", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/pedidos', methods=['GET'])
    def proxy_pedidos():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/pedidos/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/pedidos', methods=['POST'])
    def proxy_pedidos_post():
        err = _check_session()
        if err:
            return err
        data, error = api_post("/v1/pedidos/", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data), 201

    @app.route('/api/pedidos/<int:pedido_id>', methods=['GET'])
    def proxy_pedido_get(pedido_id):
        err = _check_session()
        if err:
            return err
        data, error = api_get(f"/v1/pedidos/{pedido_id}")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/pedidos/<int:pedido_id>', methods=['PUT'])
    def proxy_pedido_put(pedido_id):
        err = _check_session()
        if err:
            return err
        data, error = api_put(f"/v1/pedidos/{pedido_id}", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/detalles_pedidos', methods=['GET'])
    def proxy_detalles_pedidos():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/detalles_pedidos/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/detalles_pedidos', methods=['POST'])
    def proxy_detalles_pedidos_post():
        err = _check_session()
        if err:
            return err
        data, error = api_post("/v1/detalles_pedidos/", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data), 201

    @app.route('/api/categorias', methods=['GET'])
    def proxy_categorias():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/categorias/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/categorias', methods=['POST'])
    def proxy_categorias_post():
        err = _check_session()
        if err:
            return err
        data, error = api_post("/v1/categorias/", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/categorias/<int:cat_id>', methods=['PUT'])
    def proxy_categorias_put(cat_id):
        err = _check_session()
        if err:
            return err
        data, error = api_put(f"/v1/categorias/{cat_id}", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/categorias/<int:cat_id>', methods=['DELETE'])
    def proxy_categorias_delete(cat_id):
        err = _check_session()
        if err:
            return err
        data, error = api_delete(f"/v1/categorias/{cat_id}")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/marcas', methods=['GET'])
    def proxy_marcas():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/marcas/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/usuarios', methods=['GET'])
    def proxy_usuarios():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/usuarios/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/usuarios', methods=['POST'])
    def proxy_usuarios_post():
        err = _check_session()
        if err:
            return err
        data, error = api_post("/v1/usuarios/", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/usuarios/<int:usu_id>', methods=['PUT'])
    def proxy_usuarios_put(usu_id):
        err = _check_session()
        if err:
            return err
        data, error = api_put(f"/v1/usuarios/{usu_id}", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/estatus_pedido', methods=['GET'])
    def proxy_estatus_pedido():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/estatus_pedido/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/estatus_pedido', methods=['POST'])
    def proxy_estatus_post():
        err = _check_session()
        if err:
            return err
        data, error = api_post("/v1/estatus_pedido/", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/estatus_pedido/<int:est_id>', methods=['PUT'])
    def proxy_estatus_put(est_id):
        err = _check_session()
        if err:
            return err
        data, error = api_put(f"/v1/estatus_pedido/{est_id}", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/estatus_pedido/<int:est_id>', methods=['DELETE'])
    def proxy_estatus_delete(est_id):
        err = _check_session()
        if err:
            return err
        data, error = api_delete(f"/v1/estatus_pedido/{est_id}")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/direcciones', methods=['GET'])
    def proxy_direcciones():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/direcciones/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/roles', methods=['GET'])
    def proxy_roles():
        err = _check_session()
        if err:
            return err
        data, error = api_get("/v1/roles/")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/roles', methods=['POST'])
    def proxy_roles_post():
        err = _check_session()
        if err:
            return err
        data, error = api_post("/v1/roles/", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/roles/<int:rol_id>', methods=['PUT'])
    def proxy_roles_put(rol_id):
        err = _check_session()
        if err:
            return err
        data, error = api_put(f"/v1/roles/{rol_id}", request.get_json())
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)

    @app.route('/api/roles/<int:rol_id>', methods=['DELETE'])
    def proxy_roles_delete(rol_id):
        err = _check_session()
        if err:
            return err
        data, error = api_delete(f"/v1/roles/{rol_id}")
        if error:
            return jsonify({"error": error}), 502
        return jsonify(data)