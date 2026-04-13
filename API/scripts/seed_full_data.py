#!/usr/bin/env python3
import os
import sys
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

from database.db import SessionLocal
from database.categoria import Categoria
from database.marca import Marca
from database.autoparte import Autoparte
from database.ubicacion import Ubicacion
from database.inventario import Inventario

def main():
    db = SessionLocal()
    try:
        # Check if we already have data
        if db.query(Autoparte).count() > 0:
            print("Datos ya existen en Autopartes. Semilla ignorada para no duplicar.")
            return

        # 1. Categorías
        nombres_cat = ["Motor", "Frenos", "Suspensión", "Transmisión", "Sistema Eléctrico", "Carrocería", "Accesorios"]
        categorias = []
        for n in nombres_cat:
            cat = db.query(Categoria).filter_by(nombre=n).first()
            if not cat:
                cat = Categoria(nombre=n)
                db.add(cat)
            categorias.append(cat)
        db.flush()

        # 2. Marcas
        nombres_marca = ["Toyota", "Nissan", "Ford", "Bosch", "Brembo", "ACDelco", "LUK", "NGK", "Valeo"]
        marcas = []
        for n in nombres_marca:
            marca = db.query(Marca).filter_by(nombre=n).first()
            if not marca:
                marca = Marca(nombre=n)
                db.add(marca)
            marcas.append(marca)
        db.flush()

        # 3. Ubicaciones
        ubicaciones = []
        for pasillo in ["A", "B", "C"]:
            for estante in ["1", "2", "3"]:
                for nivel in ["Alto", "Medio", "Bajo"]:
                    ub = db.query(Ubicacion).filter_by(pasillo=pasillo, estante=estante, nivel=nivel).first()
                    if not ub:
                        ub = Ubicacion(pasillo=pasillo, estante=estante, nivel=nivel, capacidad=100, descripcion=f"Sección {pasillo}-{estante}-{nivel}")
                        db.add(ub)
                    ubicaciones.append(ub)
        db.flush()

        # 4. Autopartes e Inventarios
        productos = [
            ("Bomba de Agua", "Motor"),
            ("Pastillas de Freno", "Frenos"),
            ("Disco de Freno Ranurado", "Frenos"),
            ("Amortiguador Hidráulico", "Suspensión"),
            ("Kit de Embrague", "Transmisión"),
            ("Alternador 12V", "Sistema Eléctrico"),
            ("Batería LTH 600 Amp", "Sistema Eléctrico"),
            ("Bujía Iridium", "Motor"),
            ("Faro Delantero LED", "Carrocería"),
            ("Aceite Sintético 5W-30", "Accesorios"),
            ("Filtro de Aire", "Motor"),
            ("Radiador de Aluminio", "Motor"),
            ("Espejo Retrovisor Izquierdo", "Carrocería"),
            ("Baleros Rueda Delantera", "Suspensión"),
            ("Tensor de Banda de Tiempo", "Motor"),
            ("Bomba de Gasolina", "Motor"),
            ("Liquido de Frenos DOT-4", "Frenos"),
            ("Motor de Arranque", "Sistema Eléctrico"),
            ("Bobina de Encendido", "Sistema Eléctrico"),
            ("Sensor de Oxígeno", "Transmisión")
        ]

        autopartes = []
        for i, (nombre, cat_nombre) in enumerate(productos):
            cat_obj = next(c for c in categorias if c.nombre == cat_nombre)
            marca_obj = random.choice(marcas)
            precio = round(random.uniform(150.0, 4500.0), 2)
            
            auto = Autoparte(
                sku_codigo=f"SKU-MAC-{1000 + i}",
                nombre=f"{nombre} {marca_obj.nombre}",
                descripcion=f"Pieza genuina y certificada. {nombre} excelente para refacciones.",
                precio_unitario=precio,
                imagen_url=f"https://via.placeholder.com/300?text={nombre.replace(' ', '+')}",
                categoria_id=cat_obj.id,
                marca_id=marca_obj.id
            )
            db.add(auto)
            autopartes.append(auto)
        
        db.flush()

        # Inventarios
        for auto in autopartes:
            ub = random.choice(ubicaciones)
            inv = Inventario(
                autoparte_id=auto.id,
                ubicacion_id=ub.id,
                stock_actual=random.randint(5, 50),
                stock_minimo=random.randint(2, 5),
                pasillo=ub.pasillo,
                estante=ub.estante,
                nivel=ub.nivel
            )
            db.add(inv)

        db.commit()
        print("OK: ¡Semilla de datos cargada al 100%! Categorías, Marcas, Autopartes, Ubicaciones e Inventarios listos.")
    except Exception as e:
        db.rollback()
        print(f"Error al poblar la base de datos: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
