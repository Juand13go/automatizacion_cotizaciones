from fastapi import APIRouter, Depends
from database import get_session
from app.servicio.conversacion import obtener_o_crear_conversacion, obtener_historial_conversacion, guardado_mensajes, actualizacion_estado, creacion_lead
from app.servicio.conversacion import comunicacion_agente
import uuid

router = APIRouter()

@router.post('/conversacion')
def busqueda_creacion_conversacion(canal_user_id:str, canal:str, nombre:str, session = Depends(get_session)):
    return obtener_o_crear_conversacion(canal_user_id, canal, nombre, session)

@router.get('/historial')
def cargar_historial(id_conversacion: uuid.UUID, session = Depends(get_session)):
    return obtener_historial_conversacion(id_conversacion, session)

@router.post('/guardar_mensaje')
def guardar_mensaje(id_conversacion: uuid.UUID, rol:str, contenido:str, session = Depends(get_session)):
    return guardado_mensajes(id_conversacion, rol, contenido, session)

@router.put('/estado')
def actualizar_estado(estado: str, id_conversacion: uuid.UUID, session = Depends(get_session)):
    return actualizacion_estado(estado, id_conversacion, session)

@router.post('/crear_lead')
def creacion_de_leads(id_conversacion: uuid.UUID, productos_interes: str, ciudad: str, session = Depends(get_session)):
    return creacion_lead(id_conversacion, productos_interes, ciudad, session)

@router.post('/procesar')
def procesar(id_conversacion: uuid.UUID,  session = Depends(get_session)):
    return comunicacion_agente(id_conversacion, session)

