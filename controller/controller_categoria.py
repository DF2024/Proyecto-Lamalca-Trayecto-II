from model import Modelo_categoria

class Controlador_categoria:
    def __init__(self):
        self.modelo = Modelo_categoria()

    def crear_categoria(self, id_categoria, nombre, descripcion):
        return self.modelo.Insert(id_categoria, nombre, descripcion)

    def obtener_categoria(self, id_categoria):
        return self.modelo.Select(id_categoria)

    def obtener_todas_las_categorias(self):
        return self.modelo.Select_all()

    def actualizar_categoria(self, id_categoria, nombre, descripcion):
        return self.modelo.Update(id_categoria, nombre, descripcion)

    def eliminar_categoria(self, id_categoria):
        return self.modelo.Delete(id_categoria)
