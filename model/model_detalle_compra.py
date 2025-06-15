import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_detalle_compra(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_detalle, id_compra, id_producto, cantidad, precio_unitario):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO detalle_compra (id_detalle, id_compra, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_detalle, id_compra, id_producto, cantidad, precio_unitario))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select_all_by_compra(self, id_compra):
        cursor = self.con.cursor()
        sql = "SELECT * FROM detalle_compra WHERE id_compra = %s"
        cursor.execute(sql, (id_compra,))
        info = cursor.fetchall()
        cursor.close()
        return info
    
    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM detalle_compra"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def Delete_all_by_compra(self, id_compra):
        cursor = self.con.cursor()
        sql = "DELETE FROM detalle_compra WHERE id_compra = %s"
        cursor.execute(sql, (id_compra,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
