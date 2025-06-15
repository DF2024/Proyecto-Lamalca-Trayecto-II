import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_proveedor(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_proveedor, nombre, telefono, correo, direccion):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO proveedores (id_proveedor, nombre, telefono, correo, direccion)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_proveedor, nombre, telefono, correo, direccion))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select(self, id_proveedor):
        cursor = self.con.cursor()
        sql = "SELECT * FROM proveedores WHERE id_proveedor = %s"
        cursor.execute(sql, (id_proveedor,))
        info = cursor.fetchone()
        cursor.close()
        return info

    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM proveedores"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info

    def Update(self, id_proveedor, nombre, telefono, correo, direccion):
        cursor = self.con.cursor()
        sql = '''
            UPDATE proveedores
            SET nombre = %s, telefono = %s, correo = %s, direccion = %s
            WHERE id_proveedor = %s
        '''
        cursor.execute(sql, (nombre, telefono, correo, direccion, id_proveedor))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado

    def Delete(self, id_proveedor):
        cursor = self.con.cursor()
        sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
        cursor.execute(sql, (id_proveedor,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
