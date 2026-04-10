#!/usr/bin/env python3
"""
FASE 1: crea todas las tablas definidas en SQLAlchemy y aplica seed mínimo si la BD está vacía.

Uso (contenedor API, WORKDIR /app):
  python scripts/init_db.py

Uso local (con PostgreSQL accesible en DATABASE_URL):
  cd API && python scripts/init_db.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

from database.db import Base, SessionLocal, engine  # noqa: E402
from database import *  # noqa: E402, F401, F403
from database.seed_fase1 import aplicar_seed_si_vacio  # noqa: E402


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        aplicar_seed_si_vacio(db)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print("OK: tablas creadas o ya existentes; seed aplicado si roles estaban vacíos.")


if __name__ == "__main__":
    main()
