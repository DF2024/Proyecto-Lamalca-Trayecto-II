import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error


class Modelo_compra(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_compra,id_cliente, fecha, total):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO compras (id_compra, id_cliente, fecha, total)
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_compra, id_cliente, fecha, total))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select(self, id_compra):
        cursor = self.con.cursor()
        sql = "SELECT * FROM compras WHERE id_compra = %s"
        cursor.execute(sql, (id_compra,))
        info = cursor.fetchone()
        cursor.close()
        return info

    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM compras"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info

    def Update(self, id_compra, fecha, total, id_cliente):
        cursor = self.con.cursor()
        sql = '''
            UPDATE compras
            SET id_cliente = %s, fecha = %s, total = %s
            WHERE id_compra = %s
        '''
        cursor.execute(sql, (fecha, total, id_cliente, id_compra))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado

    def Delete(self, id_compra):
        cursor = self.con.cursor()
        sql = "DELETE FROM compras WHERE id_compra = %s"
        cursor.execute(sql, (id_compra,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
