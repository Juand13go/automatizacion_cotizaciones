# from asyncio import tools      CON ASINCRONISMO
# import anthropic
import uuid
from sqlmodel import select
from fastapi import FastAPI, Depends
from database import get_session
from models import conversaciones, mensajes, leads, productos
import os
import json
from openai import OpenAI

app = FastAPI()

@app.post('/conversacion')
def busquedaCreacionConversacion(canal_user_id:str, canal:str, nombre:str, session = Depends(get_session)):
    conversacion = session.exec(select(conversaciones).where(conversaciones.canal_user_id == canal_user_id)).first()
    if conversacion:
        return conversacion
    else: 
        nueva_conversacion = conversaciones(canal_user_id = canal_user_id, canal = canal, nombre = nombre) 
        session.add(nueva_conversacion) 
        session.commit()
        session.refresh(nueva_conversacion)
        return nueva_conversacion
    
@app.get('/historial')
def cargarHistorial(id_conversacion: uuid.UUID, session = Depends(get_session)):
    ultimosDiez = session.exec(select(mensajes).where(mensajes.id_conversacion == id_conversacion).order_by(mensajes.creado_en.desc()).limit(10)).all()
    return ultimosDiez

@app.post('/guardarMensaje')
def guardarMensaje(id_conversacion: uuid.UUID, rol:str, contenido:str, session = Depends(get_session)): 
    nuevoMensaje = mensajes(id_conversacion=id_conversacion, rol=rol, contenido=contenido)
    session.add(nuevoMensaje)
    session.commit()
    session.refresh(nuevoMensaje)
    return nuevoMensaje

@app.put('/estado')
def actualizacionEstado(estado : str, id_conversacion : uuid.UUID, session = Depends(get_session)):
    conversacion = session.exec(select(conversaciones).where(conversaciones.id_conversacion == id_conversacion)).first()
    conversacion.estado = estado
    session.add(conversacion)
    session.commit()
    session.refresh(conversacion)
    return conversacion

@app.post('/crearLead')
def crearLead(id_conversacion: uuid.UUID, productos_interes: str, ciudad: str, estado: str, session = Depends(get_session)):
    lead = leads(id_conversacion=id_conversacion, productos_interes = productos_interes, ciudad = ciudad, estado = estado)
    session.add(lead)
    session.commit() 
    session.refresh(lead)
    return lead

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

@app.post('/procesar')
def procesar(id_conversacion: uuid.UUID,  session = Depends(get_session)):
    producto = session.exec(select(productos)).all()
    catalogoProductos = [f" Producto: {c.nombre_producto} | Precio Regular:  {c.precio_regular} | Precio venta:  {c.precio_venta} | Categoría: {c.categoria} " for c in producto]
    historial = cargarHistorial(id_conversacion=id_conversacion, session=session)
    if historial == []:  #Es mas de python usar if not historial:
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
            messages=[ {"role": "system", "content": "Eres el agente encargado del manejo de cotizaciones de Industrias Rambler S.A, vas a recibir el historial de un chat con los mensajes del cliente + el catalogo con los productos: \n" + "\n".join(catalogoProductos) + "Ten en cuenta que el publico al que te diriges es de Colombia, tienes cuatro funciones (dos de ellas no obligatorias), empieza el chat saludando al cliente y preguntandole por su ubicación (La retornaras en ciudad, pero en caso de que no conteste con esa respuesta, a ciudad le asignas None) , retornar los productos de interes en caso de que el cliente los mencione sino retornas None, entregar una respuesta para enviarla al chat con el cliente, y la segunda es entregar un valor booleano marcando el estado de escalación del lead, marca True si el cliente muestra clara intención de compra (ej. quiere dejar sus datos, pide cotización formal, pregunta dónde pagar), si está muy enojado o si pide explicitamente hablar con un asesor humano. De lo contrario, marca False" + "El mensaje de texto amigable, comercial y profesional que el bot le enviará al usuario por Telegram respondiendo sus dudas usando el catalogo"}] + [{"role" : m.rol, "content" : m.contenido} for m in reversed(historial)],
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
                                    "type" : "string",
                                    "description" : "Retornar los productos de interes del cliente."
                                },
                                "ciudad" : {
                                    "type" : "string",
                                    "description" : "Ciudad desde donde el cliente realiza el contacto."
                                },
                                "debe_escalar" : {
                                    "type" : "boolean",
                                    "description" : "Marca True si el cliente muestra clara intención de compra (ej. quiere dejar sus datos, pide cotización formal, pregunta dónde pagar), si está muy enojado o si pide explicitamente hablar con un asesor humano. De lo contrario, marca False"
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
            "respuesta" : datos_parseados["respuesta_cliente"], 
            "escalar" : datos_parseados.get(["debe_escalar"] in [True, False, "True", "False", "true", "false"], False), 
            "productos_interes": datos_parseados.get("productos_interes", None),
            "ciudad": datos_parseados.get("ciudad", None) #.get() Retorna None si el campo no existe.
        }
    


# client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))     CON ASINCRONISMO
# client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) CON EL API DE CLAUDE/ANTHROPIC
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))   CON EL API DE OPEN AI

# @app.post('/procesar')
# # async def procesar(id_conversacion: uuid.UUID,  session = Depends(get_session)):    CON ASINCRONISMO
# def procesar(id_conversacion: uuid.UUID,  session = Depends(get_session)):
#     producto = session.exec(select(productos)).all()
#     catalogoProductos = [f" Producto: {c.nombre_producto} | Precio Regular:  {c.precio_regular} | Precio venta:  {c.precio_venta} | Categoría: {c.categoria} " for c in producto]
#     # historial = await cargarHistorial(id_conversacion=id_conversacion, session=session)  //CON ASINCRONISMO
#     historial = cargarHistorial(id_conversacion=id_conversacion, session=session)
#     # response = await client.messages.create(                CON ASINCRONISMO
#     response = client.messages.create(
#         model = "claude-sonnet-4-20250514",
#         max_tokens = 1024,
#         system = "Eres el agente encargado del manejo de cotizaciones de Industrias Rambler S.A, vas a recibir el historial de un chat con los mensajes del cliente + el catalogo con los productos" + "Ten en cuenta que el publico al que te diriges es de Colombia, tienes dos funciones, entregar una respuesta para enviarla al chat con el cliente, y la segunda es entregar un valor booleano marcando el estado de escalación del lead, marca True si el cliente muestra clara intención de compra (ej. quiere dejar sus datos, pide cotización formal, pregunta dónde pagar), si está muy enojado o si pide explicitamente hablar con un asesor humano. De lo contrario, marca False" + "El mensaje de texto amigable, comercial y profesional que el bot le enviará al usuario por Telegram respondiendo sus dudas usando el catalogo" + "\n".join(catalogoProductos),
#         # # EL CAMINO LARGO TRADICIONAL
#         # historial_claude = []  # 1. Creas una lista vacía

#         # for m in historial:  # 2. Recorres tus modelos de la base de datos
#         #     # 3. Creas el diccionario con el formato que Claude entiende
#         #     diccionario_mensaje = {"role": m.rol, "content": m.contenido}
#         #     # 4. Lo metes a la lista
#         #     historial_claude.append(diccionario_mensaje)
#         messages=[{"role": m.rol, "content": m.contenido} for m in reversed(historial)],
#         tools=[
#             {
#                 "name" : "evaluar_y_responder",
#                 "description" : "Herramienta obligatoria para generar la respuesta al cliente de Industrias Rambler S.A y decidir si se requiere atención humana.",

#                 "input_schema":{
#                     "type" : "object",
                    
#                     "properties" : {
#                         "respuesta_cliente" : {
#                             "type" : "string",
#                             "description" : "El mensaje de texto amigable, comercial y profesional que el bot le enviará al usuario por Telegram respondiendo sus dudas usando el catalogo"
#                         },
#                         "debe_escalar" : {
#                             "type" : "boolean",
#                             "description" : "Marca True si el cliente muestra clara intención de compra (ej. quiere dejar sus datos, pide cotización formal, pregunta dónde pagar), si está muy enojado o si pide explicitamente hablar con un asesor humano. De lo contrario, marca False"
#                         }
#                     },
#                     "required" : ["respuesta_cliente", "debe_escalar"]
#                 }
#             }
#         ],
#         tool_choice={"type": "tool", "name": "evaluar_y_responder"}
#     )
#     texto_respuesta = response.content[0].input
#     return {
#         "respuesta" : texto_respuesta["respuesta_cliente"],
#         "escalar" : texto_respuesta["debe_escalar"]      
#     }