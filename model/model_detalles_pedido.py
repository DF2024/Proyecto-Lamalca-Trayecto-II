# id_detalle int AI PK 
# id_pedido int 
# id_producto int 
# cantidad int 
# precio_unitario_venta

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error



class Model_detalles_pedido(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_detalle, id_pedido, id_producto, cantidad, precio_unitario):    


        try:
            cursor = self.con.cursor()
            sql = '''  
                INSERT INTO detalles_pedido (id_detalle, id_pedido, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_detalle, id_pedido, id_producto, cantidad, precio_unitario))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select(self, id_detalle):
        cursor = self.con.cursor()
        sql = "SELECT * FROM detalles_pedido WHERE id_detalle = %s"
        cursor.execute(sql, (id_detalle,))
        info = cursor.fetchone()
        cursor.close()
        return info
    
    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM detalles_pedido"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info
    

    def Update(self, id_detalle, id_pedido, id_producto, cantidad, precio_unitario):
        cursor = self.con.cursor()
        sql = '''
            UPDATE detalles_pedido
            SET cantidad = %s, precio_unitario = %s
        '''
        cursor.execute(sql, (id_detalle, id_pedido, id_producto, cantidad, precio_unitario))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
    
    def Delete(self, id_detalle):
        cursor = self.con.cursor()
        sql = "DELETE FROM detalles_pedido WHERE id_producto = %s"
        cursor.execute(sql, (id_detalle,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado 
    

pedido = Model_detalles_pedido()
resultado = pedido.Insert(2, 1, 1561, 2, 2000)
print(resultado)



