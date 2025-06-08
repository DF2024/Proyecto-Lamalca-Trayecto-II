import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Model_proovedores(Conexion):

    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_proovedores , nombre, telefono, direccion):

        try: 
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO proovedores (id_proovedores ,nombre, telefono, direccion)
                VALUES (%s,%s,%s,%s)
            '''
            cursor.execute(sql, (id_proovedores,nombre, telefono, direccion))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"
        
    def Select(self, id_proovedores):
        cursor = self.con.cursor()
        sql = "SELECT * FROM proovedores WHERE id_proovedores = %s"
        cursor.execute(sql, (id_proovedores,))
        info = cursor.fetchone()
        cursor.close()
        return info
    
    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM proovedores"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info
    
    def Update(self, id_proovedores, nombre, telefono, direccion):
        cursor = self.con.cursor()
        sql = '''
            UPDATE proovedores
            SET nombre = %s, telefono = %s, direccion = %s
            WHERE id_proovedores = %s
        '''
        cursor.execute(sql, (id_proovedores ,nombre, direccion, telefono))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
    
    def Delete(self, id_proovedores):
        cursor = self.con.cursor()
        sql = "DELETE FROM proovedores WHERE id_proovedores = %s"
        cursor.execute(sql, (id_proovedores,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado 
    
