import os
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session #Pausa la función y entrega la sesión al endpoint. Cuando el endpoint termina, la función continúa y el with cierra la sesión automáticamente.

