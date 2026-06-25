CREATE DATABASE n8n_bd;

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
);

INSERT INTO productos (id_woocommerce, nombre_producto, precio_regular, precio_venta, categoria) VALUES (1, 'Colchon R1', 6793000, 2717200, 'Colchones suaves'),
                                                                                        (2, 'Colchon R22', 3426000, 1541700, 'Colchones suaves'),
                                                                                        (3, 'Colchon R5', 5740000, 2296000, 'Colchones suaves'),
                                                                                        (4, 'Pillow en Viscoelastica', 608000, 516800, 'Colchones suaves'),
                                                                                        (5, 'Pillow Relajante', 288000, 244800, 'Colchones suaves'),
                                                                                        (6, 'Colchon Confortop', 3102000, 1395900, 'Colchones semifirmes'),
                                                                                        (7, 'Colchon Flexy', 1522000, 684900, 'Colchones semifirmes'),
                                                                                        (8, 'Colchon R3', 3252000, 1463000, 'Colchones semifirmes'),
                                                                                        (9, 'Colchon R30 1P', 3216000, 1447200, 'Colchones semifirmes'),
                                                                                        (10,'Colchon R30 2P', 3472000, 1562400, 'Colchones semifirmes');