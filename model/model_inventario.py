import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_inventario(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()



    def Insert(self, id_inventario, id_producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor):

        cursor = None 

        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO inventario (id_inventario, id_producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor)
                VALUES (%s, %s, %s, %s, %s ,%s, %s)
            '''

            valores = (id_producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor)
            cursor.execute(sql, valores),
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al insertar producto: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Select_all(self):

        cursor = None
        try:
            cursor = self.con.cursor()
            sql = ''' SELECT id_inventario, id_producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor FROM inventario  
            '''
            cursor.execute(sql)
            info = cursor.fetchall()
            return info
        except Error as e:
            print(f"Error al seleccionar todos los productos: {e}")
            return [] # Retornar lista vacía en caso de error.
        finally:
            if cursor:
                cursor.close()

    def Uptdate(self, id_inventario ,id_producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor):
        cursor = None 
        try:
            cursor = self.con.cursor()
            sql = '''
                UPDATE inventario
                SET id_producto = %s, cantidad_actual = %s, fecha_ultima_entrada, categoria = %s, observaciones = %s proveedor = %s 
                WHERE id_inventario = %s
            '''
            valores = (id_inventario, id_producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al actualizar inventario: {e}")
            return 0
        finally: 
            if cursor: 
                cursor.close()

    def Delete(self, id_inventario):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "DELETE FROM inventario WHERE id_inventario = %s"
            cursor.execute(sql, (id_inventario,))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al eliminar producto: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def __del__(self):
        if self.con and self.con.is_connected():
            self.con.close()