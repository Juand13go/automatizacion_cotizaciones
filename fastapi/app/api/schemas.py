from pydantic import BaseModel
from typing import Optional
import uuid

class ConversacionCrear(BaseModel):
    canal_user_id : str
    canal: str
    nombre: str

class ConversacionRespuesta(BaseModel):
    id_conversacion: uuid.UUID

class MensajeRespuesta(BaseModel):
    rol : str
    contenido : str
    
class GuardarMensajeEntrada(BaseModel):
    id_conversacion : uuid.UUID
    rol : str
    contenido : str

class EstadoEntrada(BaseModel):
    estado : str
    id_conversacion : uuid.UUID

class EstadoSalida(BaseModel):
    estado : str

class LeadEntrada(BaseModel):
    id_conversacion: uuid.UUID
    productos_interes: str
    ciudad: str

class ProcesarEntrada(BaseModel):
    id_conversacion : uuid.UUID

class ProcesarSalida(BaseModel):
    respuesta : str
    escalar : bool
    productos_interes : Optional[str]
    ciudad : Optional[str]

class ConfirmacionRespuesta(BaseModel):
    ok: bool