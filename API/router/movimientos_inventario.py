from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.db_utils import commit_or_raise
from database.inventario import Inventario
from database.movimiento_inventario import MovimientoInventario
from models.movimiento_inventario import MovimientoInventarioCreate
from security.auth import varificar_peticion

router_movimientos = APIRouter(
    prefix="/v1/inventarios/{inventario_id}/movimientos",
    tags=["Movimientos de inventario"],
)


@router_movimientos.get("/")
def listar_movimientos(inventario_id: int, db: Session = Depends(get_db)):
    inv = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return (
        db.query(MovimientoInventario)
        .filter(MovimientoInventario.inventario_id == inventario_id)
        .order_by(MovimientoInventario.id.desc())
        .all()
    )


@router_movimientos.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(varificar_peticion)])
def registrar_movimiento(
    inventario_id: int,
    body: MovimientoInventarioCreate,
    db: Session = Depends(get_db),
):
    inv = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    cant = body.cantidad
    if body.tipo == "entrada":
        inv.stock_actual += cant
    else:
        inv.stock_actual -= cant
        if inv.stock_actual < 0:
            raise HTTPException(
                status_code=400,
                detail="La merma dejaría el stock en negativo.",
            )

    mov = MovimientoInventario(
        inventario_id=inventario_id,
        tipo=body.tipo,
        cantidad=cant,
        notas=body.notas,
        usuario_id=body.usuario_id,
    )
    db.add(mov)
    commit_or_raise(db)
    db.refresh(mov)
    db.refresh(inv)
    return {"movimiento": mov, "inventario": inv}
