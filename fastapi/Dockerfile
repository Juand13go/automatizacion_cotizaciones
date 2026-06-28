# ¿Desde qué base arrancamos? (qué versión de Python)
FROM python:3.11-slim

# ¿Dónde dentro del contenedor va a vivir tu código?
WORKDIR /app

# ¿Qué dependencias necesita instalar?
COPY requirements.txt . 
RUN pip install -r requirements.txt

# ¿Qué archivos de tu proyecto copia adentro?
COPY . .

# ¿Qué comando arranca la aplicación?
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload