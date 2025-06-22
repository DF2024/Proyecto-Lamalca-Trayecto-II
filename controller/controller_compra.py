# controller/controller_compra.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_compra import Modelo_compra

class Controlador_compra:
    def __init__(self):
        self.modelo = Modelo_compra()

    def registrar_compra(self, id_cliente, id_producto, cantidad, fecha, total):
        return self.modelo.Insert(id_cliente, id_producto, cantidad, fecha, total)

    def obtener_todas_las_compras(self):
        return self.modelo.Select_all()

    def actualizar_compra(self, id_compra, id_cliente, id_producto, cantidad, fecha, total):
        return self.modelo.Update(id_compra, id_cliente, id_producto, cantidad, fecha, total)

    def eliminar_compra(self, id_compra):
        return self.modelo.Delete(id_compra)