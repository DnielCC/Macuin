from fastapi import HTTPException, Depends, APIRouter
from models.estatus_pedido import EstatusPedidoBase
from security.auth import varificar_peticion
from database.db import get_db
from database.estatus_pedido import EstatusPedido
from sqlalchemy.orm import Session

routerest = APIRouter(
    prefix="/v1/estatus_pedido",
    tags=["CRUD ESTATUS PEDIDO"]
)

@routerest.get("/")
def obtener_estatus(db: Session = Depends(get_db)):
    return db.query(EstatusPedido).all()

@routerest.get("/{estatus_id}")
def obtener_estatus_por_id(estatus_id: int, db: Session = Depends(get_db)):
    estatus = db.query(EstatusPedido).filter(EstatusPedido.id == estatus_id).first()
    if not estatus:
        raise HTTPException(status_code=404, detail="Estatus no encontrado")
    return estatus

@routerest.post("/")
def crear_estatus(estatus: EstatusPedidoBase, db: Session = Depends(get_db)):
    nuevo = EstatusPedido(**estatus.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Estatus creado", "estatus": nuevo}

@routerest.put("/{estatus_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_estatus(estatus_id: int, estatus_actualizado: EstatusPedidoBase, db: Session = Depends(get_db)):
    estatus = db.query(EstatusPedido).filter(EstatusPedido.id == estatus_id).first()
    if not estatus:
        raise HTTPException(status_code=404, detail="Estatus no encontrado")
    for key, value in estatus_actualizado.model_dump().items():
        setattr(estatus, key, value)
    db.commit()
    db.refresh(estatus)
    return {"mensaje": "Estatus actualizado", "estatus": estatus}

@routerest.delete("/{estatus_id}", dependencies=[Depends(varificar_peticion)])
def borrar_estatus(estatus_id: int, db: Session = Depends(get_db)):
    estatus = db.query(EstatusPedido).filter(EstatusPedido.id == estatus_id).first()
    if not estatus:
        raise HTTPException(status_code=404, detail="Estatus no encontrado")
    db.delete(estatus)
    db.commit()
    return {"mensaje": "Estatus eliminado"}