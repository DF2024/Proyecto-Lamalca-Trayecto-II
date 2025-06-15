from model import Modelo_compra

class Controlador_compra:
    def __init__(self):
        self.modelo = Modelo_compra()

    def crear_compra(self, id_compra, id_cliente, fecha, total):
        return self.modelo.Insert(id_compra, id_cliente, fecha, total)

    def obtener_compra(self, id_compra):
        return self.modelo.Select(id_compra)

    def obtener_todas_las_compras(self):
        return self.modelo.Select_all()

    def actualizar_compra(self, id_compra, id_cliente, fecha, total):
        return self.modelo.Update(id_compra, id_cliente, fecha, total)

    def eliminar_compra(self, id_compra):
        return self.modelo.Delete(id_compra)
