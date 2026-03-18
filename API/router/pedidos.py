from sys import prefix
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List
from models.usuario import UsuarioBase
from database.db import usuarios_db
from security.auth import varificar_peticion

routerped = APIRouter(
    prefix = "/v1/pedidos",
    tags = ["HTTP CRUD"]
)

#ENDPOINT PEDIDOS
#1- obtener todos los pedidos
@routerped.get("/")
def obtener_pedidos():
    return pedidos_db

#2- obtener pedido por id
@routerped.get("/{pedido_id}")
def obtener_pedido_por_id(pedido_id: int):
    pedido = next((p for p in pedidos_db if p["id"] == pedido_id), None)
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return pedido

#3- crear nuevo pedido
@routerped.post("/")
def crear_pedido(pedido: PedidoBase):
    nuevo_id = max(p["id"] for p in pedidos_db) + 1 if pedidos_db else 1
    nuevo_pedido = {"id": nuevo_id, **pedido.model_dump()}
    pedidos_db.append(nuevo_pedido)
    return nuevo_pedido

#4- cambiar estatus pedido
@routerped.put("/{pedido_id}/estatus", dependencies=[Depends(varificar_peticion)])
def cambiar_estatus_pedido(pedido_id: int, nuevo_estatus: str):
    for index, p in enumerate(pedidos_db):
        if p["id"] == pedido_id:
            pedidos_db[index]["estatus"] = nuevo_estatus
            return {"mensaje": "Estatus actualizado", "pedido": pedidos_db[index]}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")