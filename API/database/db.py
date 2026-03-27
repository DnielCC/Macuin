from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1. Definimos la URL de conexión (Puerto 5433 para tu instancia de PostgreSQL)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://macuin:123456@localhost:5433/DB_macuin"
)

# 2. Crear el motor de conexion
engine = create_engine(DATABASE_URL)

# 3. Preparamos el gestionador de sesiones
SessionLocal = sessionmaker(
    autocommit=False, # ninguna confirmación a la base de datos es automática
    autoflush=False, # ninguna modificación es automática
    bind=engine # definir motor en uso
)

# 4. Base declarativa del modelo
Base = declarative_base()

# 5. Obtener sesiones de cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db # cede el control a la sesión de cada petición
    finally:
        db.close()