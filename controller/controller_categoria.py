import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.model_categoria import Modelo_categoria

class Controlador_categoria:
    def __init__(self):
        self.modelo = Modelo_categoria()

    def insertar_categoria(self, id_categoria, nombre):
        return self.modelo.Insert(id_categoria, nombre)

    def obtener_categoria(self, id_categoria):
        return self.modelo.Select(id_categoria)

    def obtener_todas_las_categorias(self):
        return self.modelo.Select_all()

    def actualizar_categoria(self, id_categoria, nombre):
        return self.modelo.Update(id_categoria, nombre)

    def eliminar_categoria(self, id_categoria):
        return self.modelo.Delete(id_categoria)
