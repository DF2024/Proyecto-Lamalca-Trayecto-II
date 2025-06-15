import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_producto(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO productos (id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select(self, id_producto):
        cursor = self.con.cursor()
        sql = "SELECT * FROM productos WHERE id_producto = %s"
        cursor.execute(sql, (id_producto,))
        info = cursor.fetchone()
        cursor.close()
        return info

    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info

    def Update(self, id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor):
        cursor = self.con.cursor()
        sql = '''
            UPDATE productos
            SET nombre = %s, descripcion = %s, precio = %s, stock = %s, id_categoria = %s, id_proveedor = %s
            WHERE id_producto = %s
        '''
        cursor.execute(sql, (nombre, descripcion, precio, stock, id_categoria, id_proveedor, id_producto))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado

    def Delete(self, id_producto):
        cursor = self.con.cursor()
        sql = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(sql, (id_producto,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
