from fastapi import APIRouter
import os

routerRedi = APIRouter(
    prefix="/v1/redirect",
    tags=["Redirects"]
)

@routerRedi.get("/personal")
async def get_personal_redirect():
    flask_url = os.getenv("FLASK_URL", "http://localhost:5000")
    return {"url": f"{flask_url}/login"}