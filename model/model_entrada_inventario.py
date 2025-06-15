import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_entrada_inventario(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_entrada, fecha, id_proveedor):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO entradas_inventario (id_entrada, fecha, id_proveedor)
                VALUES (%s, %s, %s)
            '''
            cursor.execute(sql, (id_entrada, fecha, id_proveedor))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM entradas_inventario"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info

    def Delete(self, id_entrada):
        cursor = self.con.cursor()
        sql = "DELETE FROM entradas_inventario WHERE id_entrada = %s"
        cursor.execute(sql, (id_entrada,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
