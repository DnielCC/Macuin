import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.autoparte import Autoparte
from database.carrito import Carrito, CarritoLinea
from database.db import get_db
from database.db_utils import commit_or_raise
from models.carrito import CarritoCreate, CarritoLineaCreate
from security.auth import varificar_peticion

router_carritos = APIRouter(prefix="/v1/carritos", tags=["Carritos"])


@router_carritos.get("/")
def listar_carritos(db: Session = Depends(get_db), limite: int = 100):
    return db.query(Carrito).order_by(Carrito.id.desc()).limit(min(limite, 500)).all()


@router_carritos.get("/{carrito_id}")
def obtener_carrito(carrito_id: int, db: Session = Depends(get_db)):
    c = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    lineas = db.query(CarritoLinea).filter(CarritoLinea.carrito_id == carrito_id).all()
    return {"carrito": c, "lineas": lineas}


@router_carritos.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_carrito(body: CarritoCreate, db: Session = Depends(get_db)):
    uid = body.uuid or str(uuid.uuid4())
    c = Carrito(
        uuid=uid,
        laravel_user_id=body.laravel_user_id,
        email_invitado=body.email_invitado,
    )
    db.add(c)
    commit_or_raise(db)
    db.refresh(c)
    return c


@router_carritos.post(
    "/{carrito_id}/lineas",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(varificar_peticion)],
)
def agregar_linea(carrito_id: int, body: CarritoLineaCreate, db: Session = Depends(get_db)):
    c = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    if not db.query(Autoparte).filter(Autoparte.id == body.autoparte_id).first():
        raise HTTPException(status_code=400, detail="Autoparte no existe")
    linea = CarritoLinea(
        carrito_id=carrito_id,
        autoparte_id=body.autoparte_id,
        cantidad=body.cantidad,
        precio_unitario=body.precio_unitario,
    )
    db.add(linea)
    commit_or_raise(db)
    db.refresh(linea)
    return linea


@router_carritos.get("/por-usuario/{laravel_user_id}")
def obtener_carrito_por_usuario(laravel_user_id: int, db: Session = Depends(get_db)):
    """Busca el carrito más reciente de un usuario Laravel y devuelve sus líneas con info de autoparte."""
    c = (
        db.query(Carrito)
        .filter(Carrito.laravel_user_id == laravel_user_id)
        .order_by(Carrito.id.desc())
        .first()
    )
    if not c:
        return None
    lineas = db.query(CarritoLinea).filter(CarritoLinea.carrito_id == c.id).all()
    lineas_out = []
    for ln in lineas:
        ap = db.query(Autoparte).filter(Autoparte.id == ln.autoparte_id).first()
        inv = None
        if ap:
            from database.inventario import Inventario
            inv = db.query(Inventario).filter(Inventario.autoparte_id == ap.id).first()

        cat_data = None
        marca_data = None
        if ap:
            from database.categoria import Categoria
            from database.marca import Marca
            cat = db.query(Categoria).filter(Categoria.id == ap.categoria_id).first()
            marca = db.query(Marca).filter(Marca.id == ap.marca_id).first()
            if cat:
                cat_data = {"id": cat.id, "nombre": cat.nombre}
            if marca:
                marca_data = {"id": marca.id, "nombre": marca.nombre}

        lineas_out.append({
            "id": ln.id,
            "carrito_id": ln.carrito_id,
            "autoparte_id": ln.autoparte_id,
            "cantidad": ln.cantidad,
            "precio_unitario": float(ln.precio_unitario),
            "autoparte": {
                "id": ap.id,
                "sku_codigo": ap.sku_codigo,
                "nombre": ap.nombre,
                "descripcion": ap.descripcion,
                "precio_unitario": float(ap.precio_unitario),
                "imagen_url": ap.imagen_url,
                "categoria_id": ap.categoria_id,
                "marca_id": ap.marca_id,
                "categoria": cat_data,
                "marca": marca_data,
                "inventario": {
                    "id": inv.id,
                    "stock_actual": inv.stock_actual,
                    "stock_minimo": inv.stock_minimo,
                } if inv else None,
            } if ap else None,
        })

    return {
        "id": c.id,
        "uuid": c.uuid,
        "laravel_user_id": c.laravel_user_id,
        "email_invitado": c.email_invitado,
        "lineas": lineas_out,
    }


@router_carritos.patch(
    "/{carrito_id}/lineas/{linea_id}", dependencies=[Depends(varificar_peticion)]
)
def actualizar_cantidad_linea(
    carrito_id: int, linea_id: int, cantidad: int = 1, db: Session = Depends(get_db)
):
    """Actualiza la cantidad de una línea existente."""
    linea = (
        db.query(CarritoLinea)
        .filter(CarritoLinea.id == linea_id, CarritoLinea.carrito_id == carrito_id)
        .first()
    )
    if not linea:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    linea.cantidad = cantidad
    commit_or_raise(db)
    db.refresh(linea)
    return linea


@router_carritos.delete(
    "/{carrito_id}/lineas/{linea_id}", dependencies=[Depends(varificar_peticion)]
)
def quitar_linea(carrito_id: int, linea_id: int, db: Session = Depends(get_db)):
    linea = (
        db.query(CarritoLinea)
        .filter(
            CarritoLinea.id == linea_id,
            CarritoLinea.carrito_id == carrito_id,
        )
        .first()
    )
    if not linea:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    db.delete(linea)
    commit_or_raise(db)
    return {"ok": True}
