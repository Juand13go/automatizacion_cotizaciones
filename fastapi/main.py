from fastapi import FastAPI
from app.api.rutas import router
from fastapi.responses import JSONResponse
from app.excepciones import ConversacionNoEncontrada
import logging

logging.basicConfig(level=logging.ERROR)

app = FastAPI()
app.include_router(router)

@app.exception_handler(ConversacionNoEncontrada)
def manejar_conversacion_no_encontrada(request, exc):
    return JSONResponse(status_code=404, content={"detail":"Conversación No Encontrada"})

