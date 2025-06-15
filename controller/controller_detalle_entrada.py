from model import Modelo_detalle_entrada

class Controlador_detalle_entrada:
    def __init__(self):
        self.modelo = Modelo_detalle_entrada()

    def crear_detalle_entrada(self, id_detalle, id_entrada, id_producto, cantidad, precio_unitario):
        return self.modelo.Insert(id_detalle, id_entrada, id_producto, cantidad, precio_unitario)

    def obtener_detalle_entrada(self, id_detalle):
        return self.modelo.Select(id_detalle)

    def obtener_todos_los_detalles(self):
        return self.modelo.Select_all()

    def actualizar_detalle_entrada(self, id_detalle, id_entrada, id_producto, cantidad, precio_unitario):
        return self.modelo.Update(id_detalle, id_entrada, id_producto, cantidad, precio_unitario)

    def eliminar_detalle_entrada(self, id_detalle):
        return self.modelo.Delete(id_detalle)
