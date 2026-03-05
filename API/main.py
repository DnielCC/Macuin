#importaciones
from fastapi import FastAPI, status, HTTPException, Depends #<-- Importamos depens para autenticación
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials # Importamos las librerias para autenticación básica
import secrets # Importamos secrets para comparar credenciales de forma segura

#Instancia del servidor
app= FastAPI(
    title= "API Macuin",
    version="1.0"
)

#Endpoints usuarios
@app.get("/usuarios")
async def obtener_usuarios():  
    return ""