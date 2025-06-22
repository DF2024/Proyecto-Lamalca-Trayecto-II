# controller/controller_proveedor.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_proovedor import Modelo_proveedor

class Controlador_proveedor:
    def __init__(self):
        self.modelo = Modelo_proveedor()

    def insertar_proveedor(self, rif, nombre, telefono, direccion):
        return self.modelo.Insert(rif, nombre, telefono, direccion)

    def obtener_todos_los_proveedores(self):
        return self.modelo.Select_all()

    def obtener_proveedor_por_rif(self, rif):
        return self.modelo.Select_por_rif(rif)

    def actualizar_proveedor_por_rif(self, rif, nombre, telefono, direccion):
        return self.modelo.Update_por_rif(rif, nombre, telefono, direccion)

    def eliminar_proveedor_por_rif(self, rif):
        return self.modelo.Delete_por_rif(rif)