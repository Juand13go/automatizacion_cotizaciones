from sqlmodel import select, Session
from models import productos
import json
from database import engine

with open("productos.json", encoding="utf-8") as f: 
    datos = json.load(f)

def poblar_productos():
    with Session(engine) as session:
        for prod in datos:
            existe = session.exec(select(productos).where(productos.id_woocommerce == prod["id_woocommerce"])).first()
            if not existe:
                producto = productos(**prod)
                # producto = productos(id_woocommerce = prod["id_woocommerce"], nombre_producto = prod["nombre_producto"], precio_regular = prod["precio_regular"], precio_venta = prod["precio_venta"], categoria = prod["categoria"])
                session.add(producto)
                print(f"El producto {prod['nombre_producto']} fue agregado con éxito.")
            else: 
                print(f"El producto {prod['nombre_producto']} ya existe en la base de datos.")
        session.commit()

if __name__ == "__main__":
    poblar_productos()

