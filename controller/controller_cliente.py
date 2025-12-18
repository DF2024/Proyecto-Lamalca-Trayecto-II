# Archivo: controller/controller_cliente.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_cliente import Modelo_cliente

class Controlador_cliente:
    def __init__(self):
        self.modelo = Modelo_cliente()

    def insertar_cliente(self, nombre, apellido, cedula, telefono, direccion, correo):

        filas_afectadas = self.modelo.Insert(nombre, apellido, cedula, telefono, direccion, correo)
        if filas_afectadas > 0:
            return True, ""
        else:
            return False, "No se pudo agregar el cliente. Revise los datos o contacte al administrador."

    def obtener_cliente_por_cedula(self, cedula):
        return self.modelo.Select_por_cedula(cedula)

    def obtener_todos_los_clientes(self):
        return self.modelo.Select_all()

    def verificar_existencia_cedula(self, cedula):
        cliente = self.modelo.Select_por_cedula(cedula)
        return cliente is not None

    def actualizar_cliente_por_cedula(self, nombre, apellido, cedula, telefono, direccion, correo):
        return self.modelo.Update_por_cedula(nombre, apellido, cedula, telefono, direccion, correo)

    def eliminar_cliente_por_cedula(self, cedula):
        return self.modelo.Delete_por_cedula(cedula)