# Archivo: controller/controller_inventario.py
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_inventario import Modelo_inventario

class Controlador_inventario:
    def __init__(self):
        self.modelo = Modelo_inventario()

    def insertar_inventario(self, producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor):
        """
        Inserta un nuevo registro. El orden de los argumentos es el estándar en toda la app.
        """
        return self.modelo.Insert(producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor)
        
    def obtener_inventario(self, id_inventario): 
        # Esta función no se usa en la vista, pero la dejamos por si acaso.
        return self.modelo.Select(id_inventario)
    
    def verificar_existencia_producto(self, nombre_producto, id_a_excluir=None):
        producto_existente = self.modelo.buscar_por_nombre(nombre_producto, id_a_excluir)
        return producto_existente is not None

    
    def verificar_existencia_producto(self, nombre_producto, id_a_excluir=None):
        """
        Llama al modelo para verificar si un producto ya existe por su nombre.
        Acepta un ID opcional para excluirlo de la búsqueda (útil al actualizar).
        Retorna True si existe, False si no.
        """
        # Pasa ambos argumentos al modelo. Si id_a_excluir es None, el modelo lo manejará.
        producto_existente = self.modelo.buscar_por_nombre(nombre_producto, id_a_excluir)
        return producto_existente is not None
    
    def obtener_todo_inventario(self):
        return self.modelo.Select_all()

    def actualizar_inventario(self, id_inventario, producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor):
        """
        Actualiza un registro existente. El orden de los argumentos es el estándar en toda la app.
        """
        return self.modelo.Update(id_inventario, producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor)
    
    def eliminar_inventario(self, id_inventario):
        return self.modelo.Delete(id_inventario)