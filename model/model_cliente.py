from conexion import Conexion
from mysql.connector import Error

class Modelo_cliente(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self,id_cliente, nombre, apellido, cedula, telefono, direccion):
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO clientes ( id_cliente, nombre, apellido, cedula, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, ( id_cliente, nombre, apellido, cedula, telefono, direccion))
            self.con.commit()
            resultado = cursor.rowcount
            cursor.close()
            return resultado
        except Error as e:
            return f"Error: {e}"

    
    def Select_por_cedula(self, cedula):
        cursor = self.con.cursor()
        sql = "SELECT * FROM clientes WHERE cedula = %s"
        cursor.execute(sql, (cedula,))
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

    
    
    def Update_por_cedula(self, nombre, apellido, cedula, telefono, direccion):
        cursor = self.con.cursor()
        sql = '''
            UPDATE clientes
            SET nombre = %s, apellido = %s, telefono = %s, direccion = %s
            WHERE cedula = %s
        '''
        cursor.execute(sql, (nombre, apellido, telefono, direccion, cedula))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado
    
    def Delete_por_cedula(self, cedula):
        cursor = self.con.cursor()
        sql = "DELETE FROM clientes WHERE cedula = %s"
        cursor.execute(sql, (cedula,))
        self.con.commit()
        resultado = cursor.rowcount
        cursor.close()
        return resultado