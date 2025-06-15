import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error


class Modelo_categoria(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_categoria, nombre):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO categorias (id_categoria, nombre)
                VALUES (%s, %s)
            '''
            cursor.execute(sql, (id_categoria, nombre))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select(self, id_categoria):
        cursor = self.con.cursor()
        sql = "SELECT * FROM categorias WHERE id_categoria = %s"
        cursor.execute(sql, (id_categoria,))
        info = cursor.fetchone()
        cursor.close()
        return info

    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM categorias"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info

    def Update(self, id_categoria, nombre):
        cursor = self.con.cursor()
        sql = '''
            UPDATE categorias
            SET nombre = %s
            WHERE id_categoria = %s
        '''
        cursor.execute(sql, (nombre, id_categoria))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado

    def Delete(self, id_categoria):
        cursor = self.con.cursor()
        sql = "DELETE FROM categorias WHERE id_categoria = %s"
        cursor.execute(sql, (id_categoria,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
