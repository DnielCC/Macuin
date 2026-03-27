# IMPORTACIONES
from fastapi import FastAPI
from router import usuarios, autopartes, pedidos, redireccion, categorias, marcas, roles, direcciones, inventarios

app = FastAPI(
    title="API MACUIN AUTOPARTES",
    description="API para la gestion de autopartes",
    version="1.0.0"
    )

#INCLUIR ROUTERS
app.include_router(usuarios.routerusu)
app.include_router(autopartes.routerauto)
app.include_router(pedidos.routerped)
app.include_router(redireccion.routerRedi)
app.include_router(categorias.routercat)
app.include_router(marcas.routermarca)
app.include_router(roles.routerrol)
app.include_router(direcciones.routerdir)
app.include_router(inventarios.routerinv)