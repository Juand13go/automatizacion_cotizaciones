# Nombre del Proyecto
Este sistema plantea la automatizacion del apartado de cotizaciones de la empresa Industrias Rambler S.A
El flujo inicia con un mensaje del cliente por alguno de los canales de la empresa, la informacion de la conversacion es almacenada en una BD,
esta informacion se recibe y procesa en el archivo python (donde vive el agente de ia), este archivo entrega la respuesta del agente (lead), luego esta respuesta es 
almacenada en la BD, el flujo determina si escalar el lead a un humano o entregarle una respuesta el mismo, finalmente se le responde al cliente por el mismo canal por el que 
envió el mensaje (humano o agente), actualizacion estado conversacion.

This system proposes the automation of the quotations section of the company Industrias Rambler S.A
The flow starts with the customer's message through one of the company's channels, the conversation info is stored in a DATABASE, this info is received and processed in the
python file (where the AI agent lives), this file delivers the agent's response (lead), then that response is stored in the DB, the flow decides if it has to scale to a human or if he has to respond by himself, finally the customer receives a response through the same channel that he used to contact RAMBLER S.A.

## Arquitectura
POSTGRESQL BD (SISTEMA GESTOR DE DATOS) (DATA MANAGEMENT SYSTEM)
n8n (Tecnologia para la automatizacion de flujos y tareas repetitivas (BASE DEL PROYECTO)) (Technology to automate flows and repetitive tasks) (BASE OF THE PROJECT)
FastAPI-Python (Framework - Usado para la logica del proyecto) (Framework - used to build the project logic)
Claude api key (LLM, AGENTE IA) (LLM, AI AGENT)
Docker (Herramienta escencial para mantenibilidad, una arquitectura limpia y para facil acceso al proyecto en cualquier maquina)
(An essential tool for maintainability, a clean architecture, and easy access to the project on any machine.)

## Requisitos
El sistema corre en docker, esta tecnologia se encarga de que el sistema funcione sin tener que instalar nada, pero las dependencias del proyecto estan en el 
requirements.txt

The system runs on docker, this technology ensures the system runs without installing anything, but project dependencies are in requirements.txt file.

## Configuración
TOKEN TELEGRAM BOT
NOMBRE DB, USER, PASSWORD PARA POSTGRESQL Y LA N8N_DB (DB NAME, USER, PASSWORD FOR POSTGRESQL)
API KEY CLAUDE 
CONSUMER KEY Y SECRET DE WOOCOMMERCE

## Cómo levantar el entorno
Clonar el repositorio (Clone the repository)
Crear el .env (Create the .env's file)
docker compose up 

## Estructura del proyecto

El dockerfile construye el servicio de fastapi. (Dockerfile builds the fastapi's service)
El main.py almacena toda la logica de procesamiento y manipulacion de la informacion de la conversación (Main.py stores all the logic for processing and manipulating the information in the conversation)
init.sql CREACION BD DE N8N (N8N'S DB CREATION)
esquemaBD.sql CREACION BD SERVICIO GENERAL POSTGRESQL (POSTGRESQL GENERAL SERVICE CREATION)
docker-compose.yml Configuracion del docker (Docker's configuration)