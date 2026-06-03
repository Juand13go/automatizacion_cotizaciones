from datetime import datetime
import uuid
from uuid import UUID, uuid4
from typing import Optional
from decimal import Decimal
from sqlmodel import SQLModel, Field

class conversaciones(SQLModel, table=True):
    id_conversacion: UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    canal: str 
    canal_user_id: str
    nombre: Optional[str] = None
    estado: str = Field(default="activo")
    conv_actualizado_en: datetime = Field(default_factory=datetime.now)

class mensajes(SQLModel, table=True):
    id_mensaje: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_conversacion: UUID = Field(foreign_key="conversaciones.id_conversacion")
    rol: str
    contenido: str
    creado_en : datetime = Field(default_factory=datetime.now)

class leads(SQLModel, table=True):
    id_lead: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_conversacion: UUID = Field(foreign_key="conversaciones.id_conversacion")
    productos_interes: str
    ciudad: str
    estado: str
    lead_creado_en: datetime = Field(default_factory=datetime.now)

class productos(SQLModel, table=True):
    id_woocommerce: int = Field(primary_key=True)
    nombre_producto: str
    precio_regular: Decimal
    precio_venta: Decimal
    categoria: str
    actualizado_en: datetime = Field(default_factory=datetime.now)

