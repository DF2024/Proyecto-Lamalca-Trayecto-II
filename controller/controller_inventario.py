import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.model_inventario import Modelo_inventario


class Controlador_inventario:

    def __init__(self):

        self.modelo = Modelo_inventario()


    def insertar_inventario(self,  producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor):

        return self.modelo.Insert( producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor)
        
    def obtener_inventario(self, id_inventario): 

        return self.modelo.Select(id_inventario)
        
    def obtener_todo_inventario(self):

        return self.modelo.Select_all()

    def actualizar_inventario(self ,producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor):

        return self.modelo.Update(producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor)
    
    def eliminar_producto(self, id_inventario):
        return self.modelo.Delete(id_inventario)
