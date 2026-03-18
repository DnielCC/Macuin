from sys import prefix
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List
from models.usuario import UsuarioBase
from database.db import usuarios_db
from security.auth import varificar_peticion

routerusu = APIRouter(
    prefix = "/v1/usuarios",
    tags = ["HTTP CRUD"]
)

#ENDPOINT USUARIOS
#1- todos los usuarios
@routerusu.get("/")
async def leer_usuarios():
    return {
        "total":len(usuarios_db),
        "usuarios":usuarios_db,
        "status":"200"
    }

#2- usuario por id
@routerusu.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    usuario = next((u for u in usuarios_db if u["id"] == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

#3- crear usuario
@routerusu.post("/")
def crear_usuario(usuario: UsuarioBase):
    nuevo_id = max(u["id"] for u in usuarios_db) + 1 if usuarios_db else 1
    nuevo_usuario = {"id": nuevo_id, **usuario.model_dump()}
    usuarios_db.append(nuevo_usuario)
    return {"mensaje": "Usuario creado", "usuario": nuevo_usuario}

#4- Modificar usuario
@routerusu.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario_actualizado: UsuarioBase):
    for index, u in enumerate(usuarios_db):
        if u["id"] == usuario_id:
            usuarios_db[index].update(usuario_actualizado.model_dump())
            return {"mensaje": "Usuario actualizado", "usuario": usuarios_db[index]}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#5- eliminar usuario
@routerusu.delete("/{usuario_id}", dependencies=[Depends(varificar_peticion)])
def borrar_usuario(usuario_id: int):
    for index, u in enumerate(usuarios_db):
        if u["id"] == usuario_id:
            del usuarios_db[index]
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")