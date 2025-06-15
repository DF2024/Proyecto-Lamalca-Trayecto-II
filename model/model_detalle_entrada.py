import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_detalle_entrada(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_detalle, id_entrada, id_producto, cantidad, precio_unitario):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO detalle_entrada (id_detalle, id_entrada, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_detalle, id_entrada, id_producto, cantidad, precio_unitario))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select_all_by_entrada(self, id_entrada):
        cursor = self.con.cursor()
        sql = "SELECT * FROM detalle_entrada WHERE id_entrada = %s"
        cursor.execute(sql, (id_entrada,))
        info = cursor.fetchall()
        cursor.close()
        return info
    
    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM detalle_entrada"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def Delete_all_by_entrada(self, id_entrada):
        cursor = self.con.cursor()
        sql = "DELETE FROM detalle_entrada WHERE id_entrada = %s"
        cursor.execute(sql, (id_entrada,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
