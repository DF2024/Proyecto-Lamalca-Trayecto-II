# model/model_proveedor.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_proveedor(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, rif, nombre, telefono, direccion):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO proveedores (rif, nombre, telefono, direccion)
                VALUES (%s, %s, %s, %s)
            '''
            valores = (rif, nombre, telefono, direccion)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al insertar proveedor: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Select_all(self):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "SELECT id_proveedor, rif, nombre, telefono, direccion FROM proveedores ORDER BY nombre"
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al seleccionar todos los proveedores: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def Select_por_rif(self, rif):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "SELECT id_proveedor, rif, nombre, telefono, direccion FROM proveedores WHERE rif = %s"
            cursor.execute(sql, (rif,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al buscar proveedor por RIF: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def Update_por_rif(self, rif, nombre, telefono, direccion):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = '''
                UPDATE proveedores
                SET nombre = %s, telefono = %s, direccion = %s
                WHERE rif = %s
            '''
            valores = (nombre, telefono, direccion, rif)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al actualizar proveedor: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Delete_por_rif(self, rif):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "DELETE FROM proveedores WHERE rif = %s"
            cursor.execute(sql, (rif,))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al eliminar proveedor: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            
    def __del__(self):
        if self.con and self.con.is_connected():
            self.con.close()