import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.model_cliente import Modelo_cliente

class Controlador_cliente:
    def __init__(self):
        self.modelo = Modelo_cliente()

    def insertar_cliente(self, id_cliente, nombre, apellido, cedula, telefono, direccion):
        return self.modelo.Insert(id_cliente, nombre, apellido, cedula, telefono, direccion)

    def obtener_cliente(self, id_cliente):
        return self.modelo.Select(id_cliente)

    def obtener_todos_los_clientes(self):
        return self.modelo.Select_all()

    def actualizar_cliente(self, id_cliente, nombre, apellido, cedula, telefono, direccion):
        return self.modelo.Update(id_cliente, nombre, apellido, cedula, telefono, direccion)

    def eliminar_cliente(self, id_cliente):
        return self.modelo.Delete(id_cliente)