import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_compra import Modelo_compra
from model.model_inventario import Modelo_inventario # <-- Importamos el modelo de inventario

class Controlador_compra:
    def __init__(self):
        self.modelo = Modelo_compra()
        self.modelo_inventario = Modelo_inventario() # <-- Creamos una instancia

    def registrar_compra(self, id_cliente, id_inventario, cantidad, fecha, total):
        # 1. Registrar la compra
        resultado_compra = self.modelo.Insert(id_cliente, id_inventario, cantidad, fecha, total)
        
        if resultado_compra:
            # 2. Si la compra fue exitosa, descontar del stock
            # Usamos una función que tendremos que crear en el modelo de inventario
            self.modelo_inventario.actualizar_stock(id_inventario, -cantidad) # Usamos negativo para restar
        
        return resultado_compra

    def obtener_todas_las_compras(self):
        return self.modelo.Select_all()

    def actualizar_compra(self, id_compra, id_cliente, id_inventario_nuevo, cantidad_nueva, fecha, total):
        # Lógica de actualización de stock:
        # 1. Obtener los datos de la compra original (producto y cantidad viejos)
        compra_original = self.modelo.Select_por_id(id_compra)
        if not compra_original: return False
        
        id_inventario_viejo, cantidad_vieja = compra_original

        # 2. Devolver el stock del producto original
        self.modelo_inventario.actualizar_stock(id_inventario_viejo, cantidad_vieja)

        # 3. Descontar el stock del nuevo producto
        self.modelo_inventario.actualizar_stock(id_inventario_nuevo, -cantidad_nueva)
        
        # 4. Actualizar el registro de la compra
        return self.modelo.Update(id_compra, id_cliente, id_inventario_nuevo, cantidad_nueva, fecha, total)

    def eliminar_compra(self, id_compra):
        # 1. Antes de eliminar, necesitamos saber qué producto y cantidad devolver al stock
        compra_a_eliminar = self.modelo.Select_por_id(id_compra)
        if not compra_a_eliminar: return False

        id_inventario, cantidad = compra_a_eliminar
        
        # 2. Devolvemos la cantidad al inventario
        self.modelo_inventario.actualizar_stock(id_inventario, cantidad)

        # 3. Ahora sí, eliminamos el registro de la compra
        return self.modelo.Delete(id_compra)