from fastapi import APIRouter, Depends, status
from database import get_session
from app.servicio.conversacion import obtener_o_crear_conversacion, obtener_historial_conversacion, guardado_mensajes, actualizacion_estado, creacion_lead
from app.servicio.conversacion import comunicacion_agente
import uuid
from app.api.schemas import ConversacionCrear, GuardarMensajeEntrada, EstadoEntrada, LeadEntrada, ProcesarEntrada
from app.api.schemas import ConversacionRespuesta, MensajeRespuesta, EstadoSalida, ProcesarSalida, ConfirmacionRespuesta

router = APIRouter()

@router.post('/conversacion', response_model=ConversacionRespuesta)
def busqueda_creacion_conversacion(datos: ConversacionCrear, session = Depends(get_session)):
    return obtener_o_crear_conversacion(canal_user_id=datos.canal_user_id, canal=datos.canal, nombre=datos.nombre, session=session)

@router.get('/historial', response_model=list[MensajeRespuesta])
def cargar_historial(id_conversacion: uuid.UUID, session = Depends(get_session)):
    return obtener_historial_conversacion(id_conversacion, session)

@router.post('/guardar_mensaje', response_model=ConfirmacionRespuesta)
def guardar_mensaje(datos: GuardarMensajeEntrada, session = Depends(get_session)):
    guardado_mensajes(id_conversacion=datos.id_conversacion, rol=datos.rol, contenido=datos.contenido, session=session)
    return {"ok": True}

@router.put('/estado', response_model=EstadoSalida)
def actualizar_estado(datos: EstadoEntrada, session = Depends(get_session)):
    return actualizacion_estado(estado=datos.estado, id_conversacion=datos.id_conversacion, session=session)

@router.post('/crear_lead', response_model=ConfirmacionRespuesta)
def creacion_de_leads(datos: LeadEntrada, session = Depends(get_session)):
    creacion_lead(id_conversacion=datos.id_conversacion, productos_interes=datos.productos_interes, ciudad=datos.ciudad, session=session)
    return {"ok": True}

@router.post('/procesar', response_model=ProcesarSalida)
def procesar(datos: ProcesarEntrada,  session = Depends(get_session)):
    return comunicacion_agente(id_conversacion=datos.id_conversacion, session=session)

  