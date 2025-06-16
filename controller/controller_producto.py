import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.model_producto import Modelo_producto


class Controlador_producto:
    def __init__(self):
        self.modelo = Modelo_producto()

    def insertar_producto(self, id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor):
        return self.modelo.Insert(id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor)

    def obtener_producto(self, id_producto):
        return self.modelo.Select(id_producto)

    def obtener_todos_los_productos(self):
        return self.modelo.Select_all()

    def actualizar_producto(self, id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor):
        return self.modelo.Update(id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor)

    def eliminar_producto(self, id_producto):
        return self.modelo.Delete(id_producto)
