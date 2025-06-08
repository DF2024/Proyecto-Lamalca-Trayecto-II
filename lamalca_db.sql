ALTER TABLE quimicos
ADD COLUMN id_producto INT UNIQUE,
ADD CONSTRAINT fk_producto_quimico
FOREIGN KEY (id_producto) REFERENCES productos(id_producto);