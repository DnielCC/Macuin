from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.cliente import Cliente
from database.db import get_db
from database.db_utils import commit_or_raise
from models.cliente import ClienteBase, ClienteUpdate
from security.auth import varificar_peticion

router_clientes = APIRouter(prefix="/v1/clientes", tags=["Clientes B2B"])


@router_clientes.get("/")
def listar_clientes(db: Session = Depends(get_db), solo_activos: bool = False):
    q = db.query(Cliente)
    if solo_activos:
        q = q.filter(Cliente.activo.is_(True))
    return q.order_by(Cliente.id).all()


@router_clientes.get("/{cliente_id}")
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    c = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return c


@router_clientes.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def crear_cliente(body: ClienteBase, db: Session = Depends(get_db)):
    c = Cliente(**body.model_dump())
    db.add(c)
    commit_or_raise(db)
    db.refresh(c)
    return c


@router_clientes.put("/{cliente_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_cliente(cliente_id: int, body: ClienteUpdate, db: Session = Depends(get_db)):
    c = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    commit_or_raise(db)
    db.refresh(c)
    return c


@router_clientes.patch("/{cliente_id}/baja", dependencies=[Depends(varificar_peticion)])
def baja_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Marca cliente como inactivo (soft delete)."""
    c = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    c.activo = False
    commit_or_raise(db)
    db.refresh(c)
    return c
