# IMPORTACIONES
from fastapi import FastAPI
from router import usuarios, autopartes, pedidos

app = FastAPI(
    title="API MACUIN AUTOPARTES",
    description="API para la gestion de autopartes",
    version="1.0.0"
    )

#INCLUIR ROUTERS
app.include_router(usuarios.routerusu)
app.include_router(autopartes.routerauto)
app.include_router(pedidos.routerped)