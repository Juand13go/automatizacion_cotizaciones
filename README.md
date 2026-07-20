# Automatización de Cotizaciones - Industrias Rambler S.A.
Este sistema plantea la automatización del apartado de cotizaciones de la empresa Industrias Rambler S.A.
El flujo inicia con un mensaje del cliente por alguno de los canales de la empresa (actualmente Telegram), la información de la conversación es almacenada en una BD;
esta información se recibe y procesa en el archivo de Python (donde vive el agente de IA), este archivo entrega la respuesta del agente junto con los datos del lead
(productos de interés, ciudad y si debe escalarse o no), luego esta respuesta es almacenada en la BD. El flujo determina si escalar el lead a un humano (creando el lead,
asignando un asesor y alertándolo) o entregar la respuesta él mismo; finalmente se le responde al cliente por el mismo canal por el que envió el mensaje (humano o agente)
y se actualiza el estado de la conversación.

## Arquitectura
PostgreSQL BD (Sistema gestor de datos, almacena conversaciones, mensajes, leads, asesores y el catálogo de productos)
n8n (Tecnología para la automatización de flujos y tareas repetitivas (BASE DEL PROYECTO))
FastAPI - Python (Framework - Usado para la lógica del proyecto)
Groq API (LLM, agente IA - modelo llama-3.3-70b-versatile con tool calling para estructurar la respuesta y la decisión de escalación)
Docker (Herramienta esencial para mantenibilidad, una arquitectura limpia y para fácil acceso al proyecto en cualquier máquina)
Migraciones con Alembic
Schemas de Pydantic (Validación de los datos que entran y salen)
SQLModel (ORM - Definición de las tablas y comunicación con PostgreSQL)
ngrok (Proxy inverso para exponer n8n por HTTPS y recibir el webhook de Telegram)

## Requisitos
El sistema corre en Docker, esta tecnología se encarga de que el sistema funcione sin tener que instalar nada; las dependencias del proyecto están en el
requirements.txt.
Necesitas: Docker y Docker Compose, una cuenta de ngrok, un bot de Telegram (creado con @BotFather) y una API Key de Groq.

## Configuración
Todas las variables van en un archivo .env en la raíz del proyecto:
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD (PostgreSQL)
N8N_DB, N8N_USER, N8N_PASSWORD (Base de datos y credenciales de n8n)
WEBHOOK_URL (URL HTTPS que entrega ngrok)
GROQ_API_KEY (Agente IA)

El token del bot de Telegram y el consumer key/secret de WooCommerce (sincronización del catálogo) se configuran como credenciales dentro de n8n.

## Cómo levantar el entorno
Clonar el repositorio
Crear el .env (ver sección de configuración)
Para el proxy inverso con ngrok: ngrok http 5678 (Recibirás una URL HTTPS, colócala en la variable WEBHOOK_URL del .env)
docker compose up (al arrancar se ejecutan automáticamente las migraciones con Alembic y el seed.py que puebla el catálogo de productos)
Abrir n8n en la URL de ngrok (HTTPS) e importar el archivo con el flujo 'automatizacion_cotizaciones.json' (carpeta n8n/)
Configurar la credencial de Telegram en n8n y activar el flujo
La documentación interactiva de la API queda disponible en http://localhost:8000/docs

## Estructura del proyecto
El Dockerfile construye el servicio de FastAPI.
La estructura de este proyecto está guiada por 3 capas (Servicio, Persistencia y API). En la capa de servicio encuentras toda la lógica de la aplicación (en Python nativo),
incluyendo la comunicación con el agente de IA (conversacion.py); en la capa de persistencia encuentras todos los queries y la comunicación de la aplicación con la base
de datos (repositorio.py); y finalmente tenemos la capa de API con todos los endpoints de FastAPI y los schemas de Pydantic. Los endpoints expuestos son: /conversacion
(busca o crea la conversación), /historial (mensajes de una conversación), /guardar_mensaje, /procesar (ejecuta el agente IA), /crear_lead y /estado.
En la raíz de fastapi/ están models.py (definición de las tablas con SQLModel), database.py (conexión a la BD), seed.py (inyección del catálogo desde productos.json)
y la carpeta alembic/ con las migraciones.
docker-compose.yml: Configuración del Docker y comandos de arranque y montaje de la BD (creación del esquema, inyección de datos a la BD (seed.py), arranque de la aplicación).
init.sql: Crea la base de datos exclusiva de n8n al levantar PostgreSQL por primera vez.