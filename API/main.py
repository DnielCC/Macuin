import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from router import (
    auth,
    autopartes,
    carritos,
    categorias,
    clientes,
    direcciones,
    estatus_pedido,
    guias_envio,
    inventarios,
    marcas,
    movimientos_inventario,
    movimientos_inventario_feed,
    pagos,
    parametros_sistema,
    pedidos,
    portal_contacto,
    redireccion,
    roles,
    ubicaciones,
    usuarios,
)

app = FastAPI(
    title="API MACUIN AUTOPARTES",
    description="API REST para gestión de autopartes, pedidos, inventario y portal (FASE 2).",
    version="2.0.0",
)

_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5001,http://localhost:8003,http://127.0.0.1:5001,http://127.0.0.1:8003",
)
_origins_list = [o.strip() for o in _origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def _charset_utf8_json(request, call_next):
    """Asegura charset=utf-8 en JSON para clientes que no asumen UTF-8 por defecto."""
    response = await call_next(request)
    ct = response.headers.get("content-type", "")
    if ct.startswith("application/json") and "charset" not in ct.lower():
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "Conflicto de integridad en la base de datos."},
    )


app.include_router(auth.router_auth)
app.include_router(usuarios.routerusu)
app.include_router(autopartes.routerauto)
app.include_router(pedidos.routerped)
app.include_router(redireccion.routerRedi)
app.include_router(categorias.routercat)
app.include_router(marcas.routermarca)
app.include_router(roles.routerrol)
app.include_router(direcciones.routerdir)
app.include_router(inventarios.routerinv)
app.include_router(clientes.router_clientes)
app.include_router(ubicaciones.router_ubicaciones)
app.include_router(guias_envio.router_guias)
app.include_router(movimientos_inventario.router_movimientos)
app.include_router(movimientos_inventario_feed.router_mov_feed)
app.include_router(parametros_sistema.router_parametros)
app.include_router(carritos.router_carritos)
app.include_router(pagos.router_pagos)
app.include_router(estatus_pedido.router_estatus)
app.include_router(portal_contacto.router_portal_contacto)
