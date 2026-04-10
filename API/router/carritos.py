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
