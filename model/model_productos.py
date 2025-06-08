import os 
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error
from model.model_proovedores import Model_proovedores

class Model_producto(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_producto, nombre_producto, descripcion, precio_unitario, stock, categoria_producto, id_proovedores):


        try:
            cursor = self.con.cursor()
            sql = '''  
                INSERT INTO vehiculo (id_producto, nombre_producto, descripcion, precio_unitario, stock, categoria_producto, id_proovedores)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_producto, nombre_producto, descripcion, precio_unitario, stock, categoria_producto, id_proovedores))
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
        sql = "SELECT * FROM procutos"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info
    
    def Update(self, id_producto, nombre_producto, descripcion, precio_unitario, stock, categoria_producto, id_proovedores):
        cursor = self.con.cursor()
        sql = '''
            UPDATE productos
            SET nombre_producto = %s, descripcion = %s, precio_unitario = %s, stoct = %s, categoria_producto = %s, id_proovedores = %s
            WHERE id_producto = %s
        '''
        cursor.execute(sql, (id_producto, nombre_producto, descripcion, precio_unitario, stock, categoria_producto, id_proovedores))
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