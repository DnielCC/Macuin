from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.ubicacion import Ubicacion
from models.ubicacion import UbicacionBase, UbicacionUpdate
from security.auth import varificar_peticion

router_ubicaciones = APIRouter(prefix="/v1/ubicaciones", tags=["Ubicaciones almacén"])


@router_ubicaciones.get("/")
def listar_ubicaciones(db: Session = Depends(get_db), solo_activas: bool = False):
    q = db.query(Ubicacion)
    if solo_activas:
        q = q.filter(Ubicacion.activo.is_(True))
    return q.order_by(Ubicacion.id).all()


@router_ubicaciones.get("/{ubicacion_id}")
def obtener_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    u = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return u


@router_ubicaciones.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_ubicacion(body: UbicacionBase, db: Session = Depends(get_db)):
    u = Ubicacion(**body.model_dump())
    db.add(u)
    commit_or_raise(db)
    db.refresh(u)
    return u


@router_ubicaciones.put("/{ubicacion_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_ubicacion(ubicacion_id: int, body: UbicacionUpdate, db: Session = Depends(get_db)):
    u = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(u, k, v)
    commit_or_raise(db)
    db.refresh(u)
    return u


@router_ubicaciones.delete("/{ubicacion_id}", dependencies=[Depends(varificar_peticion)])
def eliminar_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    u = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    db.delete(u)
    commit_or_raise(db)
    return {"ok": True}
