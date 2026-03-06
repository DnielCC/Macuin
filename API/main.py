# IMPORTACIONES
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API Version 1")

#DB ficticia
usuarios_db = [
    {"id": 1, "nombre": "Juan Perez", "email": "juan@macuin.com", "rol": "ADMIN"},
    {"id": 2, "nombre": "Maria Lopez", "email": "maria@cliente.com", "rol": "CLIENTE"}
]

autopartes_db = [
    {"id": 1, "sku": "BTO-001", "nombre": "Bomba de Agua", "precio": 450.50, "stock": 10},
    {"id": 2, "sku": "FRN-002", "nombre": "Balatas Delanteras", "precio": 890.00, "stock": 5}
]

pedidos_db = [
    {"id": 1, "usuario_id": 2, "total": 890.00, "estatus": "PENDIENTE"}
]

#VALIDACIÓN PYDADNTIC
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: str

class AutoparteBase(BaseModel):
    sku: str
    nombre: str
    precio: float
    stock: int

class PedidoBase(BaseModel):
    usuario_id: int
    total: float
    estatus: str

#ENDPOINT USUARIOS
#1- todos los usuarios
@app.get("/usuarios/", response_model=List[dict], tags=["Usuarios"])
def obtener_usuarios():
    return usuarios_db

#2- usuario por id
@app.get("/usuarios/{usuario_id}", tags=["Usuarios"])
def obtener_usuario(usuario_id: int):
    usuario = next((u for u in usuarios_db if u["id"] == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

#3- crear usuario
@app.post("/usuarios/", tags=["Usuarios"])
def crear_usuario(usuario: UsuarioBase):
    nuevo_id = max(u["id"] for u in usuarios_db) + 1 if usuarios_db else 1
    nuevo_usuario = {"id": nuevo_id, **usuario.model_dump()}
    usuarios_db.append(nuevo_usuario)
    return {"mensaje": "Usuario creado", "usuario": nuevo_usuario}

#4- Modificar usuario
@app.put("/usuarios/{usuario_id}", tags=["Usuarios"])
def actualizar_usuario(usuario_id: int, usuario_actualizado: UsuarioBase):
    for index, u in enumerate(usuarios_db):
        if u["id"] == usuario_id:
            usuarios_db[index].update(usuario_actualizado.model_dump())
            return {"mensaje": "Usuario actualizado", "usuario": usuarios_db[index]}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#5- eliminar usuario
@app.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def borrar_usuario(usuario_id: int):
    for index, u in enumerate(usuarios_db):
        if u["id"] == usuario_id:
            del usuarios_db[index]
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#ENDPOINTS AUTOPARTES

#1- obtener todas las autopartes
@app.get("/autopartes/", tags=["Autopartes"])
def obtener_autopartes():
    return autopartes_db

#2- buscar autoparte por nombre
@app.get("/autopartes/buscar/", tags=["Autopartes"])
def buscar_autoparte_por_nombre(nombre: str):
    resultados = [a for a in autopartes_db if nombre.lower() in a["nombre"].lower()]
    
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron autopartes con ese nombre")
    
    return resultados

#3- crear nueva autoparte
@app.post("/autopartes/", tags=["Autopartes"])
def crear_autoparte(autoparte: AutoparteBase):
    nuevo_id = max(a["id"] for a in autopartes_db) + 1 if autopartes_db else 1
    nueva_autoparte = {"id": nuevo_id, **autoparte.model_dump()}
    autopartes_db.append(nueva_autoparte)
    return nueva_autoparte

#4- actualizar autoparte
@app.put("/autopartes/{autoparte_id}", tags=["Autopartes"])
def actualizar_autoparte(autoparte_id: int, auto_act: AutoparteBase):
    for index, a in enumerate(autopartes_db):
        if a["id"] == autoparte_id:
            autopartes_db[index].update(auto_act.model_dump())
            return autopartes_db[index]
    raise HTTPException(status_code=404, detail="Autoparte no encontrada")

#5- eliminar autoparte
@app.delete("/autopartes/{autoparte_id}", tags=["Autopartes"])
def borrar_autoparte(autoparte_id: int):
    for index, a in enumerate(autopartes_db):
        if a["id"] == autoparte_id:
            del autopartes_db[index]
            return {"mensaje": "Autoparte eliminada"}
    raise HTTPException(status_code=404, detail="Autoparte no encontrada")

#ENDPOINTS PEDIDOS
#1- obtener todos los pedidos
@app.get("/pedidos/", tags=["Pedidos"])
def obtener_pedidos():
    return pedidos_db

#2- obtener pedido por id
@app.get("/pedidos/{pedido_id}", tags=["Pedidos"])
def obtener_pedido_por_id(pedido_id: int):
    pedido = next((p for p in pedidos_db if p["id"] == pedido_id), None)
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return pedido

#3- crear nuevo pedido
@app.post("/pedidos/", tags=["Pedidos"])
def crear_pedido(pedido: PedidoBase):
    nuevo_id = max(p["id"] for p in pedidos_db) + 1 if pedidos_db else 1
    nuevo_pedido = {"id": nuevo_id, **pedido.model_dump()}
    pedidos_db.append(nuevo_pedido)
    return nuevo_pedido

#4- cambiar estatus pedido
@app.put("/pedidos/{pedido_id}/estatus", tags=["Pedidos"])
def cambiar_estatus_pedido(pedido_id: int, nuevo_estatus: str):
    for index, p in enumerate(pedidos_db):
        if p["id"] == pedido_id:
            pedidos_db[index]["estatus"] = nuevo_estatus
            return {"mensaje": "Estatus actualizado", "pedido": pedidos_db[index]}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")