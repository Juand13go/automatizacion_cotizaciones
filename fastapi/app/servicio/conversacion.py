from sqlmodel import Session
from app.persistencia.repositorio import creacion_conversacion, verificacion_existencia_conversacion, historial_conversacion, guardar_mensaje_por_rol
from app.persistencia.repositorio import crear_lead, actualizar_estado_conversacion, obtener_productos
import uuid
from openai import OpenAI
import json
import os

def obtener_o_crear_conversacion(canal_user_id: str, canal: str, nombre: str, session):
    conversacion = verificacion_existencia_conversacion(canal_user_id, session)
    if conversacion:
        return conversacion
    else: 
        return creacion_conversacion(canal_user_id, canal, nombre, session)

def obtener_historial_conversacion(id_conversacion: uuid.UUID, session: Session):
    return historial_conversacion(id_conversacion, session)

def guardado_mensajes(id_conversacion: uuid.UUID, rol:str, contenido:str, session: Session):
    return guardar_mensaje_por_rol(id_conversacion, rol, contenido, session)

def actualizacion_estado(estado: str, id_conversacion: uuid.UUID, session: Session):
    return actualizar_estado_conversacion(estado, id_conversacion, session)

def creacion_lead(id_conversacion: uuid.UUID, productos_interes: str, ciudad: str, session: Session):
    return crear_lead(id_conversacion, productos_interes, ciudad, session)

def catalogo_a_texto(session: Session):
    producto = obtener_productos(session)
    catalogo_productos = [f" Producto: {c.nombre_producto} | Precio Regular:  {c.precio_regular} | Precio venta:  {c.precio_venta} | Categoría: {c.categoria} " for c in producto]
    catalogo_productos_variable = "\n".join(catalogo_productos)
    return catalogo_productos_variable

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

def comunicacion_agente(id_conversacion: uuid.UUID, session: Session):
    historial = obtener_historial_conversacion(id_conversacion=id_conversacion, session=session)
    catalogo_productos_variable = catalogo_a_texto(session) 
    if not historial:  #Es mas de python usar if not historial: que es lo mismo que if historial == []:
        return {
            "respuesta": "¡Hola! Bienvenido a Industrias Rambler S.A. ¿Desde qué ciudad nos contactas?",
            "escalar": False,
            "productos_interes": None,
            "ciudad": None
        }
    else:
        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            max_tokens = 1024,
            messages=[{
                        "role": "system", "content": f"""Eres el agente encargado del manejo de cotizaciones de Industrias Rambler S.A, vas a recibir el historial de un chat con 
                        los mensajes del cliente + el catalogo con los productos: {catalogo_productos_variable} Ten en cuenta que el publico al que te diriges es de Colombia, empieza el chat saludando al cliente y preguntandole por su ubicación 
                        (La retornaras en ciudad, pero en caso de que no conteste con esa respuesta AÚN, a ciudad le asignas valor None (no me refiero a un valor vacío, me refiero 
                        al tipo de dato None)), retornar los productos de interes en caso de que el cliente los mencione si no retornas None (no me refiero a un valor vacío, 
                        me refiero al tipo de dato None), entregar una respuesta para enviarla al chat con el cliente; entregar un valor booleano marcando el estado de escalación 
                        del lead, marca True (Como booleano) si el cliente muestra clara intención de compra (ej. quiere dejar sus datos, pide cotización formal, pregunta dónde 
                        pagar), si está muy enojado o si pide explicitamente hablar con un asesor humano; OBSERVACION IMPORTANTE: JAMAS ESCALES A TRUE CON LOS CAMPOS "productos_interes" o "ciudad" vacíos, NO escales todavía: tu tarea es preguntárselo de forma amable en respuesta_cliente. Solo marca debe_escalar: True cuando ya tengas ambos datos... De lo contrario, marca False (Como booleano). El mensaje de texto 
                        amigable, comercial y profesional que el bot le enviará al usuario por Telegram respondiendo sus dudas usando el catalogo"""
            }] + [{"role" : m.rol, "content" : m.contenido} for m in reversed(historial)],
            tools=[
                {
                    "type" : "function",
                    "function": {

                        "name" : "evaluar_y_responder",
                        "description" : "Herramienta obligatoria para generar la respuesta al cliente de Industrias Rambler S.A y decidir si se requiere atención humana.",

                        "parameters":{
                            "type" : "object",
                            
                            "properties" : {
                                "respuesta_cliente" : {
                                    "type" : "string",
                                    "description" : "El mensaje de texto amigable, comercial y profesional que el bot le enviará al usuario por Telegram respondiendo sus dudas usando el catalogo"
                                },
                                "productos_interes" : {
                                    "type" : ["string", "null"],
                                    "description" : "Retornar los productos de interes del cliente."
                                },
                                "ciudad" : {
                                    "type" : ["string", "null"],
                                    "description" : "Ciudad desde donde el cliente realiza el contacto."
                                },
                                "debe_escalar" : {
                                    "type" : "boolean",
                                    "description" : "Marca True si el cliente muestra clara intención de compra. De lo contrario, marca False"
                                }
                            },
                            "required" : ["respuesta_cliente", "debe_escalar"]
                        }
                    }
                }
            ],
            tool_choice={"type": "function", "function": {"name": "evaluar_y_responder"}}
        )
        texto_respuesta = response.choices[0].message.tool_calls[0].function.arguments
        datos_parseados = json.loads(texto_respuesta)

        return {
            "respuesta" : datos_parseados.get("respuesta_cliente", ""), 
            "escalar" : True if (datos_parseados.get("debe_escalar", False) in [True, "True", "true"]) else False,
            "productos_interes": datos_parseados.get("productos_interes", None),
            "ciudad": datos_parseados.get("ciudad", None) 
        }
