# controller/controller_categoria.py

import os
import sys

# Asegura que se pueda acceder a los módulos en el directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa la clase del modelo correspondiente
from model.model_categoria import Modelo_categoria

class Controlador_categoria:
    """
    El Controlador actúa como intermediario entre la Vista y el Modelo.
    No contiene lógica de negocio compleja, solo delega las peticiones
    de la vista hacia el modelo apropiado.
    """
    def __init__(self):
        """
        Al inicializarse, el controlador crea una instancia del modelo
        para poder interactuar con la base de datos a través de él.
        """
        self.modelo = Modelo_categoria()

    def insertar_categoria(self, nombre):
        """
        Pasa la solicitud de insertar una nueva categoría al modelo.
        """
        # La vista solo proporciona el nombre, ya que el ID es autoincremental.
        return self.modelo.Insert(nombre)

    def obtener_categoria(self, id_categoria):
        """
        Pasa la solicitud de obtener una única categoría por su ID al modelo.
        (Este método no es usado por la CategoriaView actual, pero es una buena práctica tenerlo).
        """
        return self.modelo.Select(id_categoria)

    def obtener_todas_las_categorias(self):
        """
        Pasa la solicitud de obtener todas las categorías al modelo.
        """
        return self.modelo.Select_all()

    def actualizar_categoria(self, id_categoria, nombre):
        """
        Pasa la solicitud de actualizar una categoría al modelo.
        """
        return self.modelo.Update(id_categoria, nombre)

    def eliminar_categoria(self, id_categoria):
        """
        Pasa la solicitud de eliminar una categoría al modelo.
        """
        return self.modelo.Delete(id_categoria)