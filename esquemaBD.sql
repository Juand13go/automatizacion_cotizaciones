CREATE TABLE conversaciones (
    id_conversacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canal VARCHAR(20) NOT NULL,
    canal_user_id VARCHAR(100) NOT NULL,    
    nombre VARCHAR(200),
    estado VARCHAR(50) DEFAULT 'activo',
    conv_actualizado_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE mensajes(
    id_mensaje UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_conversacion UUID REFERENCES conversaciones(id_conversacion),
    rol VARCHAR(20),
    contenido TEXT,
    creado_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE leads(
    id_lead UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_conversacion UUID REFERENCES conversaciones(id_conversacion),
    productos_interes VARCHAR(200),
    ciudad VARCHAR(200),
    estado VARCHAR(200),
    lead_creado_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE productos(
    id_woocommerce INT PRIMARY KEY,
    nombre_producto VARCHAR(300),
    precio_regular NUMERIC(12,2),
    precio_venta NUMERIC(12,2),
    categoria VARCHAR(200),
    actualizado_en TIMESTAMP DEFAULT NOW()
)