# Nombre del Proyecto
Este sistema plantea la automatizacion del apartado de cotizaciones de la empresa Industrias Rambler S.A
El flujo inicia con un mensaje del cliente por alguno de los canales de la empresa, la informacion de la conversacion es almacenada en una BD,
esta informacion se recibe y procesa en el archivo python (donde vive el agente de ia), este archivo entrega la respuesta del agente (lead), luego esta respuesta es 
almacenada en la BD, el flujo determina si escalar el lead a un humano o entregarle una respuesta el mismo, finalmente se le responde al cliente por el mismo canal por el que 
envió el mensaje (humano o agente), actualizacion estado conversacion.

## Arquitectura
POSTGRESQL BD (SISTEMA GESTOR DE DATOS) 
n8n (Tecnologia para la automatizacion de flujos y tareas repetitivas (BASE DEL PROYECTO)) 
FastAPI-Python (Framework - Usado para la logica del proyecto) 
Claude api key (LLM, AGENTE IA) 
Docker (Herramienta escencial para mantenibilidad, una arquitectura limpia y para facil acceso al proyecto en cualquier maquina)

## Requisitos
El sistema corre en docker, esta tecnologia se encarga de que el sistema funcione sin tener que instalar nada, pero las dependencias del proyecto estan en el 
requirements.txt

## Configuración
TOKEN TELEGRAM BOT
NOMBRE DB, USER, PASSWORD PARA POSTGRESQL Y LA N8N_DB 
API KEY CLAUDE 
CONSUMER KEY Y SECRET DE WOOCOMMERCE

## Cómo levantar el entorno
Clonar el repositorio 
Crear el .env 
docker compose up 
Para el proxy inverso con ngrok: ngrok http 5678 (Recibiras una URL HTTPS, modifica la variable WEBHOOK_URL en el .env )

## Estructura del proyecto
El dockerfile construye el servicio de fastapi. 
El main.py almacena toda la logica de procesamiento y manipulacion de la informacion de la conversación 
init.sql CREACION BD DE N8N
esquemaBD.sql CREACION BD SERVICIO GENERAL POSTGRESQL
docker-compose.yml Configuracion del docker 