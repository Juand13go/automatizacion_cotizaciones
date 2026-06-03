# ¿Desde qué base arrancamos? (qué versión de Python)
# ¿Dónde dentro del contenedor va a vivir tu código?
# ¿Qué dependencias necesita instalar?
# ¿Qué archivos de tu proyecto copia adentro?
# ¿Qué comando arranca la aplicación?

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port 8000