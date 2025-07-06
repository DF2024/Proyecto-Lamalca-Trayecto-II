# Archivo: controller/controller_inventario.py
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_inventario import Modelo_inventario

class Controlador_inventario:
    def __init__(self):
        self.modelo = Modelo_inventario()

    def insertar_inventario(self, producto, cantidad, fecha, id_categoria, observaciones, id_proveedor):
        """
        Inserta un nuevo registro. El orden de los argumentos es el estándar en toda la app.
        """
        return self.modelo.Insert(producto, cantidad, fecha, id_categoria, observaciones, id_proveedor)
        
    def obtener_inventario(self, id_inventario): 
        # Esta función no se usa en la vista, pero la dejamos por si acaso.
        return self.modelo.Select(id_inventario)
        
    def obtener_todo_inventario(self):
        return self.modelo.Select_all()

    def actualizar_inventario(self, id_inventario, producto, cantidad, fecha, id_categoria, observaciones, id_proveedor):
        """
        Actualiza un registro existente. El orden de los argumentos es el estándar en toda la app.
        """
        return self.modelo.Update(id_inventario, producto, cantidad, fecha, id_categoria, observaciones, id_proveedor)
    
    def eliminar_inventario(self, id_inventario):
        return self.modelo.Delete(id_inventario)