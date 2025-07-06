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

    def Insert(self, producto, cantidad, fecha, id_categoria, observaciones, id_proveedor):
        cursor = None 
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO inventario (producto, cantidad_actual, fecha_ultima_entrada, categoria, observaciones, proveedor)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            valores = (producto, cantidad, fecha, id_categoria, observaciones, id_proveedor)
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
            sql = ''' 
                SELECT 
                    id_inventario, producto, cantidad_actual, fecha_ultima_entrada, 
                    observaciones, categoria, proveedor
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

    def Update(self, id_inventario, producto, cantidad, fecha, id_categoria, observaciones, id_proveedor):
        cursor = None 
        try:
            cursor = self.con.cursor()
            # Nombres de columnas en la BD
            sql = '''
                UPDATE inventario
                SET producto = %s, cantidad_actual = %s, fecha_ultima_entrada = %s, categoria = %s, observaciones = %s, proveedor = %s 
                WHERE id_inventario = %s
            '''
            # El orden de los valores debe coincidir con los %s. El ID para el WHERE va al final.
            valores = (producto, cantidad, fecha, id_categoria, observaciones, id_proveedor, id_inventario)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error en Modelo_inventario.Update: {e}")
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
            print(f"Error en Modelo_inventario.Delete: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def buscar_por_nombre(self, nombre_producto):

        cursor = None
        try:
            cursor = self.con.cursor()
            # Usamos LIMIT 1 porque solo necesitamos saber si existe al menos uno. Es más eficiente.
            sql = "SELECT * FROM inventario WHERE producto = %s LIMIT 1"
            cursor.execute(sql, (nombre_producto,))
            return cursor.fetchone()  # Retorna una tupla si lo encuentra, None si no.
        except Error as e:
            print(f"Error en Modelo_inventario.buscar_por_nombre: {e}")
            return None # En caso de error, asumimos que no existe para no bloquear al usuario.
        finally:
            if cursor:
                cursor.close()

    def __del__(self):
        if self.con and self.con.is_connected():
            self.con.close()