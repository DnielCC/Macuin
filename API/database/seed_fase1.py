"""Datos mínimos para desarrollo (roles, estatus, usuario sistema). Idempotente."""

from sqlalchemy.orm import Session

from database.rol import Rol
from database.estatus_pedido import EstatusPedido
from database.usuario import Usuario


def aplicar_seed_si_vacio(session: Session) -> None:
    if session.query(Rol).count() > 0:
        return

    roles = [
        Rol(
            nombre_rol="Administrador",
            descripcion="Acceso total al sistema y catálogo maestro.",
            permisos="CRUD_ALL",
        ),
        Rol(
            nombre_rol="Ventas",
            descripcion="Clientes B2B y pedidos.",
            permisos="CLIENTES,PEDIDOS,LECTURA_CATALOGO",
        ),
        Rol(
            nombre_rol="Logística",
            descripcion="Envíos, guías y estatus de entrega.",
            permisos="ENVIOS,GUIAS,LECTURA_DIRECCIONES",
        ),
        Rol(
            nombre_rol="Almacén",
            descripcion="Inventario, ubicaciones y surtido.",
            permisos="INVENTARIO,UBICACIONES,PEDIDOS_ALMACEN",
        ),
    ]
    session.add_all(roles)
    session.flush()

    estatus_filas = [
        ("Borrador", "pedido", "#94a3b8"),
        ("Pendiente", "pedido", "#f59e0b"),
        ("Confirmado", "pedido", "#3b82f6"),
        ("Surtiendo", "almacen", "#8b5cf6"),
        ("Empacado", "almacen", "#6366f1"),
        ("Enviado", "logistica", "#0ea5e9"),
        ("Entregado", "logistica", "#22c55e"),
        ("Cancelado", "pedido", "#ef4444"),
    ]
    for nombre, modulo, color in estatus_filas:
        session.add(EstatusPedido(nombre=nombre, modulo=modulo, color=color))

    session.flush()

    admin_rol = session.query(Rol).filter_by(nombre_rol="Administrador").one()
    # Hash de ejemplo (no usar en producción); sustituir por flujo real de contraseñas en FASE 2+.
    session.add(
        Usuario(
            nombre="Sistema",
            apellidos="Macuin",
            email="sistema@macuin.local",
            password_hash="SEED_CAMBIAR_CON_PASSWORD_REAL",
            telefono=None,
            rol_id=admin_rol.id,
            direccion_id=None,
            activo=True,
        )
    )
