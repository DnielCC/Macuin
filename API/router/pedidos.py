from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from models.pedido import PedidoBase
from security.auth import varificar_peticion
from database.db import get_db
from database.pedido import Pedido
from sqlalchemy.orm import Session

routerped = APIRouter(
    prefix = "/v1/pedidos",
    tags = ["HTTP CRUD"]
)

#1- obtener todos los pedidos
@routerped.get("/")
def obtener_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

#2- obtener pedido por id
@routerped.get("/{pedido_id}")
def obtener_pedido_por_id(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

#3- crear nuevo pedido
@routerped.post("/")
def crear_pedido(pedido: PedidoBase, db: Session = Depends(get_db)):
    nuevo_pedido = Pedido(**pedido.model_dump())
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return {"mensaje": "Pedido creado", "pedido": nuevo_pedido}

#4- cambiar pedido completo
@routerped.put("/{pedido_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_pedido(pedido_id: int, pedido_actualizado: PedidoBase, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for key, value in pedido_actualizado.model_dump().items():
        setattr(pedido, key, value)
    db.commit()
    db.refresh(pedido)
    return {"mensaje": "Pedido actualizado", "pedido": pedido}

#5- eliminar pedido
@routerped.delete("/{pedido_id}", dependencies=[Depends(varificar_peticion)])
def borrar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(pedido)
    db.commit()
    return {"mensaje": "Pedido eliminado"}