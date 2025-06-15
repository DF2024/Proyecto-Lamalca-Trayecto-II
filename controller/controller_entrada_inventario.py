import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.model_entrada_inventario import Modelo_entrada_inventario


class Controlador_entrada_inventario:
    def __init__(self):
        self.modelo = Modelo_entrada_inventario()

    def crear_entrada(self, id_entrada, id_proveedor, fecha, total):
        return self.modelo.Insert(id_entrada, id_proveedor, fecha, total)

    def obtener_entrada(self, id_entrada):
        return self.modelo.Select(id_entrada)

    def obtener_todas_las_entradas(self):
        return self.modelo.Select_all()

    def actualizar_entrada(self, id_entrada, id_proveedor, fecha, total):
        return self.modelo.Update(id_entrada, id_proveedor, fecha, total)

    def eliminar_entrada(self, id_entrada):
        return self.modelo.Delete(id_entrada)
