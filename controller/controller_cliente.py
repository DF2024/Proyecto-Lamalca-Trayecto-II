# Archivo: controller/controller_cliente.py

import os
import sys
from validations.client_validations import validar_cliente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_cliente import Modelo_cliente

class Controlador_cliente:
    def __init__(self):
        self.modelo = Modelo_cliente()

    def insertar_cliente(self, data):
        errores = validar_cliente(data)
        if errores:
            return False, errores  # devolvemos la tupla

        if self.modelo.existe_cedula(data["cedula"]):
            return False, ["La cédula ya existe"]

        exito = self.modelo.Insert(**data)
        if exito:
            return True, []
        else:
            return False, ["Error al insertar en la base de datos"]



    def obtener_cliente_por_cedula(self, data):
        return self.modelo.Select_por_cedula(data)

    def obtener_todos_los_clientes(self):
        return self.modelo.Select_all()

    def verificar_existencia_cedula(self, data):
        cliente = self.modelo.Select_por_cedula(data)
        return cliente is not None

    def actualizar_cliente(self, data):
            errores = validar_cliente(data)
            if errores:
                return False, errores  # tupla (ok, mensajes)

            if not self.modelo.existe_cedula(data["cedula"]):
                return False, ["No existe un cliente con esa cédula"]

            # Modelo devuelve 1 si se actualizó, 0 si no
            filas_afectadas = self.modelo.Update_por_cedula(**data)
            if filas_afectadas:
                return True, []
            else:
                return False, ["Error al actualizar en la base de datos"]

    def eliminar_cliente_por_cedula(self, data):
        return self.modelo.Delete_por_cedula(data)