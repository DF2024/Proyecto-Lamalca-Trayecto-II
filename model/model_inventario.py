# Archivo: model/model_inventario.py

import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_inventario(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    # <<-- MODIFICADO: Añadido 'precio_unitario' -->>
    def Insert(self, producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor):
        cursor = None 
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO inventario (producto, cantidad_actual, precio_unitario, fecha_ultima_entrada, categoria, observaciones, proveedor)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            valores = (producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error en Modelo_inventario.Insert: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Select_all(self):
        cursor = None
        try:
            cursor = self.con.cursor()
            # <<-- MODIFICADO: Añadido 'precio_unitario' al SELECT -->>
            sql = ''' 
                SELECT 
                    id_inventario, producto, cantidad_actual, precio_unitario, 
                    fecha_ultima_entrada, observaciones, categoria, proveedor
                FROM inventario
            '''
            cursor.execute(sql)
            info = cursor.fetchall()
            return info
        except Error as e:
            print(f"Error en Modelo_inventario.Select_all: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def actualizar_stock(self, id_inventario, cantidad_a_cambiar):
        cursor = None
        try:
            cursor = self.con.cursor()
            # Esta consulta suma o resta la cantidad al valor actual
            sql = "UPDATE inventario SET cantidad_actual = cantidad_actual + %s WHERE id_inventario = %s"
            cursor.execute(sql, (cantidad_a_cambiar, id_inventario))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al actualizar stock: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def buscar_por_nombre(self, nombre_producto, id_a_excluir=None):
        """
        Busca un producto por su nombre.
        - Si se provee un 'id_a_excluir', lo ignora en la búsqueda (útil para la actualización).
        - Retorna el producto si lo encuentra, de lo contrario retorna None.
        """
        cursor = None
        try:
            cursor = self.con.cursor()
            
            # Construcción dinámica de la consulta
            sql = "SELECT id_inventario FROM inventario WHERE producto = %s LIMIT 1"
            params = (nombre_producto,)

            if id_a_excluir is not None:
                # Si estamos actualizando, no queremos que se encuentre a sí mismo como un duplicado
                sql = "SELECT id_inventario FROM inventario WHERE producto = %s AND id_inventario != %s LIMIT 1"
                params = (nombre_producto, id_a_excluir)

            cursor.execute(sql, params)
            return cursor.fetchone()
        except Error as e:
            print(f"Error en Modelo_inventario.buscar_por_nombre: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


    # <<-- MODIFICADO: Añadido 'precio_unitario' -->>
    def Update(self, id_inventario, producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor):
        cursor = None 
        try:
            cursor = self.con.cursor()
            sql = '''
                UPDATE inventario
                SET producto = %s, cantidad_actual = %s, precio_unitario = %s, 
                    fecha_ultima_entrada = %s, categoria = %s, observaciones = %s, proveedor = %s 
                WHERE id_inventario = %s
            '''
            valores = (producto, cantidad, precio_unitario, fecha, id_categoria, observaciones, id_proveedor, id_inventario)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error en Modelo_inventario.Update: {e}")
            return 0
        finally: 
            if cursor: 
                cursor.close()

    # ... (El resto de funciones como Delete, __del__, etc., se quedan igual) ...
    def Delete(self, id_inventario):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "DELETE FROM inventario WHERE id_inventario = %s"
            cursor.execute(sql, (id_inventario,))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error en Modelo_inventario.Delete: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def __del__(self):
        if self.con and self.con.is_connected():
            self.con.close()