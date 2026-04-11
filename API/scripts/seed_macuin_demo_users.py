"""
Crea o actualiza usuarios demo para el login de Flask (contraseñas con bcrypt).

Ejecutar en el contenedor API:
  python scripts/seed_macuin_demo_users.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

from database.db import SessionLocal  # noqa: E402
from database.rol import Rol  # noqa: E402
from database.usuario import Usuario  # noqa: E402

# Hashes bcrypt generados para las contraseñas indicadas en README-CREDENCIALES.md
HASHES = {
    "admin@macuin.com": "$2b$12$KTTmNwAAVQ3yZqslVbRUPOhs90DDL1DhzI8k8doYoGqzdcEN.WL1C",  # admin123
    "ventas@macuin.com": "$2b$12$fgOtaxvyklAPkqiK1qtP7.xNjhX1bIsuMV62fhXm22I9n5uV1MEda",  # ventas123
    "logistica@macuin.com": "$2b$12$3CSUsyhFruUHIpL8g4ne2eZNu4IviiPphkDMYaR12I8x2NNk2Pq5m",  # logistica123
    "almacen@macuin.com": "$2b$12$cXSl55oqtB7f.1wSL0zfoeL5Az9c.RuUsrPI0nS.DY/F6PDrlVtOK",  # almacen123
}

DEMO = [
    ("Administrador", "Frank", "Contreras", "admin@macuin.com"),
    ("Ventas", "María", "González", "ventas@macuin.com"),
    ("Logística", "Ana", "Martínez", "logistica@macuin.com"),
    ("Almacén", "Carlos", "López", "almacen@macuin.com"),
]


def main() -> None:
    db = SessionLocal()
    try:
        for rol_nombre, nombre, apellidos, email in DEMO:
            rol = db.query(Rol).filter(Rol.nombre_rol == rol_nombre).first()
            if not rol:
                raise RuntimeError(f"No existe el rol '{rol_nombre}'. Ejecuta antes init_db/seed_fase1.")
            h = HASHES[email]
            u = db.query(Usuario).filter(Usuario.email == email).first()
            if u:
                u.nombre = nombre
                u.apellidos = apellidos
                u.rol_id = rol.id
                u.password_hash = h
                u.activo = True
            else:
                db.add(
                    Usuario(
                        nombre=nombre,
                        apellidos=apellidos,
                        email=email,
                        password_hash=h,
                        telefono=None,
                        rol_id=rol.id,
                        direccion_id=None,
                        activo=True,
                    )
                )
        db.commit()
        print("OK: usuarios demo listos para login Flask.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
