from sys import prefix
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List
from models.usuario import UsuarioBase
from security.auth import varificar_peticion
from database.db import get_db
from database.autoparte import Autoparte
from sqlalchemy.orm import Session
from models.autoparte import AutoparteBase

routerauto = APIRouter(
    prefix = "/v1/autopartes",
    tags = ["CRUD AUTOPARTES"]
)

#ENDPOINT AUTOPARTES
#1- obtener todas las autopartes
@routerauto.get("/")
def obtener_autopartes(db: Session = Depends(get_db)):
    return db.query(Autoparte).all()

#2- buscar autoparte por nombre
@routerauto.get("/buscar/")
def buscar_autoparte_por_nombre(nombre: str, db: Session = Depends(get_db)):
    resultados = db.query(Autoparte).filter(Autoparte.nombre.ilike(f"%{nombre}%")).all()
    
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron autopartes con ese nombre")
    
    return resultados

#3- crear nueva autoparte
@routerauto.post("/")
def crear_autoparte(autoparte: AutoparteBase, db: Session = Depends(get_db)):
    nueva_autoparte = Autoparte(**autoparte.model_dump())
    db.add(nueva_autoparte)
    db.commit()
    db.refresh(nueva_autoparte)
    return nueva_autoparte

#4- actualizar autoparte
@routerauto.put("/{autoparte_id}", dependencies=[Depends(varificar_peticion)])
def actualizar_autoparte(autoparte_id: int, auto_act: AutoparteBase, db: Session = Depends(get_db)  ):
    autoparte = db.query(Autoparte).filter(Autoparte.id == autoparte_id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    for key, value in auto_act.model_dump().items():
        setattr(autoparte, key, value)
    db.commit()
    db.refresh(autoparte)
    return autoparte

#5- eliminar autoparte
@routerauto.delete("/{autoparte_id}", dependencies=[Depends(varificar_peticion)])
def borrar_autoparte(autoparte_id: int, db: Session = Depends(get_db)):
    autoparte = db.query(Autoparte).filter(Autoparte.id == autoparte_id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    db.delete(autoparte)
    db.commit()
    return {"mensaje": "Autoparte eliminada"}
