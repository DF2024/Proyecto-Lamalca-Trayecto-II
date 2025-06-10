# id_cliente 
# nombre 
# apellido 
# cedula 
# telefono 
# direccion 

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_cliente(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, id_cliente, nombre, apellido, cedula, telefono, direccion):

        try:
            cursor = self.con.cursor()
            sql = '''  
                INSERT INTO clientes (id_cliente, nombre, apellido, cedula, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_cliente, nombre, apellido, cedula, telefono, direccion))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    def Select(self, id_cliente):
        cursor = self.con.cursor()
        sql = "SELECT * FROM clientes WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        info = cursor.fetchone()
        cursor.close()
        return info
    
    def Select_all(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM clientes"
        cursor.execute(sql)
        info = cursor.fetchall()
        cursor.close()
        return info
    
    def Update(self, id_cliente, nombre, apellido, cedula, telefono, direccion):
        cursor = self.con.cursor()
        sql = '''
            UPDATE clientes
            SET nombre = %s, apellido = %s, cedula = %s, telefono = %s, direccion = %s
            WHERE id_cliente = %s
        '''
        cursor.execute(sql, (id_cliente, nombre, apellido, cedula, telefono, direccion))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
    
    def Delete(self, id_producto):
        cursor = self.con.cursor()
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor.execute(sql, (id_producto,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado 
    

cliente = Modelo_cliente()
resultado = cliente.Insert('0001', 'Andrés', 'García', '30443212', '04161772078', 'La concordia')

print(resultado)