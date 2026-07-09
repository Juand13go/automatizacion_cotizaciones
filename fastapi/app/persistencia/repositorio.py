from models import conversaciones, mensajes, leads, productos
from sqlmodel import select, Session
import uuid

def verificacion_existencia_conversacion(canal_user_id:str, session: Session): 
    conversacion = session.exec(select(conversaciones).where(conversaciones.canal_user_id == canal_user_id)).first()
    return conversacion

def creacion_conversacion(canal_user_id:str, canal:str, nombre:str, session: Session):
    nueva_conversacion = conversaciones(canal_user_id = canal_user_id, canal = canal, nombre = nombre) 
    session.add(nueva_conversacion) 
    session.commit()
    session.refresh(nueva_conversacion)
    return nueva_conversacion

def historial_conversacion(id_conversacion: uuid.UUID, session: Session):
    return session.exec(select(mensajes).where(mensajes.id_conversacion == id_conversacion).order_by(mensajes.creado_en.desc()).limit(10)).all()
    
def guardar_mensaje_por_rol(id_conversacion: uuid.UUID, rol:str, contenido:str, session: Session):
    nuevo_mensaje = mensajes(id_conversacion=id_conversacion, rol=rol, contenido=contenido)
    session.add(nuevo_mensaje)
    session.commit()
    session.refresh(nuevo_mensaje)
    return nuevo_mensaje

def actualizar_estado_conversacion(estado: str, id_conversacion: uuid.UUID, session: Session):
    conversacion = session.exec(select(conversaciones).where(conversaciones.id_conversacion == id_conversacion)).first()
    conversacion.estado = estado
    session.add(conversacion)
    session.commit()
    session.refresh(conversacion)
    return conversacion

def crear_lead(id_conversacion: uuid.UUID, productos_interes: str, ciudad: str, session: Session):
    lead = leads(id_conversacion=id_conversacion, productos_interes = productos_interes, ciudad = ciudad)
    session.add(lead)
    session.commit() 
    session.refresh(lead)
    return lead

def obtener_productos(session: Session):
    return session.exec(select(productos)).all()