from fastapi import HTTPException, Depends, APIRouter
from database.db import get_db
from database.detalle_pedido import DetallePedido
from sqlalchemy.orm import Session

routerdet = APIRouter(
    prefix="/v1/detalles_pedidos",
    tags=["CRUD DETALLES PEDIDOS"]
)

@routerdet.get("/")
def obtener_detalles(db: Session = Depends(get_db)):
    return db.query(DetallePedido).all()

@routerdet.get("/{detalle_id}")
def obtener_detalle_por_id(detalle_id: int, db: Session = Depends(get_db)):
    detalle = db.query(DetallePedido).filter(DetallePedido.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle