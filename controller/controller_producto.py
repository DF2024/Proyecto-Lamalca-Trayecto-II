# controller/controller_producto.py

import os
import sys

# Asegura que se pueda acceder a los módulos en el directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa la clase del modelo correspondiente
from model.model_producto import Modelo_producto

class Controlador_producto:
    """
    El Controlador para Productos delega todas las operaciones de datos al Modelo_producto.
    """
    def __init__(self):
        """
        Crea una instancia del modelo de productos.
        """
        self.modelo = Modelo_producto()

    def insertar_producto(self, nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor):
        # CAMBIO 1: Se eliminó 'id_producto' de los parámetros.
        # El modelo ahora no lo necesita, ya que el ID es autoincremental.
        # CAMBIO 2: Se renombró 'precio' a 'precio_venta' para consistencia.
        return self.modelo.Insert(nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor)

    def obtener_producto(self, id_producto):
        # Este método no se usa en la vista actual, pero lo mantenemos por si es necesario en el futuro.
        # Suponiendo que tu modelo aún tiene el método Select(id_producto).
        return self.modelo.Select(id_producto)

    def obtener_todos_los_productos(self):
        """
        Pasa la solicitud de obtener todos los productos al modelo.
        """
        return self.modelo.Select_all()

    def actualizar_producto(self, id_producto, nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor):
        # CAMBIO 3: Se renombró 'precio' a 'precio_venta' para ser consistente
        # con el modelo y la base de datos.
        return self.modelo.Update(id_producto, nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor)

    def eliminar_producto(self, id_producto):
        """
        Pasa la solicitud de eliminar un producto al modelo.
        """
        return self.modelo.Delete(id_producto)