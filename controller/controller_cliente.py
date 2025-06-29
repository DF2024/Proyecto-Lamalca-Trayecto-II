import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.model_cliente import Modelo_cliente

class Controlador_cliente:
    def __init__(self):
        self.modelo = Modelo_cliente()

    def insertar_cliente(self, nombre, apellido, cedula, telefono, direccion):
        return self.modelo.Insert( nombre, apellido, cedula, telefono, direccion)

    def obtener_cliente_por_cedula(self, cedula):
        return self.modelo.Select_por_cedula(cedula)

    def obtener_todos_los_clientes(self):
        return self.modelo.Select_all()

    
    def actualizar_cliente_por_cedula(self, nombre, apellido, cedula, telefono, direccion):
        return self.modelo.Update_por_cedula(nombre, apellido, cedula, telefono, direccion)

    def eliminar_cliente_por_cedula(self, cedula):
        return self.modelo.Delete_por_cedula(cedula)
    
