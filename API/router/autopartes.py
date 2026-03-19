from sys import prefix
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List
from models.usuario import UsuarioBase
from database.db import usuarios_db
from security.auth import varificar_peticion

routerauto = APIRouter(
    prefix = "/v1/autopartes",
    tags = ["HTTP CRUD"]
)

#ENDPOINT AUTOPARTES
#1- obtener todas las autopartes
@routerauto.get("/")
def obtener_autopartes():
    return autopartes_db

#2- buscar autoparte por nombre
@routerauto.get("/buscar/")
def buscar_autoparte_por_nombre(nombre: str):
    resultados = [a for a in autopartes_db if nombre.lower() in a["nombre"].lower()]
    
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron autopartes con ese nombre")
    
    return resultados

#3- crear nueva autoparte
@routerauto.post("/")
def crear_autoparte(autoparte: AutoparteBase):
    nuevo_id = max(a["id"] for a in autopartes_db) + 1 if autopartes_db else 1
    nueva_autoparte = {"id": nuevo_id, **autoparte.model_dump()}
    autopartes_db.append(nueva_autoparte)
    return nueva_autoparte

#4- actualizar autoparte
@routerauto.put("/{autoparte_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_autoparte(autoparte_id: int, auto_act: AutoparteBase):
    for index, a in enumerate(autopartes_db):
        if a["id"] == autoparte_id:
            autopartes_db[index].update(auto_act.model_dump())
            return autopartes_db[index]
    raise HTTPException(status_code=404, detail="Autoparte no encontrada")

#5- eliminar autoparte
@routerauto.delete("/{autoparte_id}", dependencies=[Depends(varificar_peticion)])
def borrar_autoparte(autoparte_id: int):
    for index, a in enumerate(autopartes_db):
        if a["id"] == autoparte_id:
            del autopartes_db[index]
            return {"mensaje": "Autoparte eliminada"}
    raise HTTPException(status_code=404, detail="Autoparte no encontrada")
