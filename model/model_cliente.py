from conexion import Conexion
from mysql.connector import Error

class Modelo_cliente(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, nombre, apellido, cedula, telefono, direccion, correo):
        
        if not nombre or not apellido or not cedula:
            print("Error: Nombre, apellido y cédula son obligatorios.")
            return 0
        if not cedula.isdigit():
            print("Error: La cédula debe ser numérica.")
            return 0
        if telefono and not telefono.isdigit():
            print("Error: El teléfono debe ser numérico.")
            return 0
        
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO clientes (nombre, apellido, cedula, telefono, direccion, correo)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (nombre, apellido, cedula, telefono, direccion, correo))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error en Modelo_cliente.Insert: {e}")
            return 0 # Devuelve 0 para indicar que no se insertaron filas
        finally:
            if cursor:
                cursor.close()
    
    def Select_por_cedula(self, cedula):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM clientes WHERE cedula = %s"
            cursor.execute(sql, (cedula,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error en Modelo_cliente.Select_por_cedula: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def Select_por_id(self, id_cliente):
        cursor = None
        try:
            cursor = self.con.cursor(dictionary=True)
            sql = "SELECT *, CONCAT(nombre, ' ', apellido) as nombre_completo FROM clientes WHERE id_cliente = %s"
            cursor.execute(sql, (id_cliente,))
            return cursor.fetchone()
        finally:
            if cursor: cursor.close()

    def Select_all(self):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM clientes"
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error en Modelo_cliente.Select_all: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def buscar_por_cedula(self, cedula):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "SELECT cedula FROM clientes WHERE cedula = %s LIMIT 1" # Solo necesitamos una columna para ser más eficientes
            cursor.execute(sql, (cedula,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error en Modelo_cliente.buscar_por_cedula: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def Update_por_cedula(self, nombre, apellido, cedula, telefono, direccion, correo):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = '''
                UPDATE clientes
                SET nombre = %s, apellido = %s, telefono = %s, direccion = %s, correo = %s
                WHERE cedula = %s
            '''
            cursor.execute(sql, (nombre, apellido, telefono, direccion, correo, cedula))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error en Modelo_cliente.Update_por_cedula: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def Delete_por_cedula(self, cedula):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "DELETE FROM clientes WHERE cedula = %s"
            cursor.execute(sql, (cedula,))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error en Modelo_cliente.Delete_por_cedula: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()