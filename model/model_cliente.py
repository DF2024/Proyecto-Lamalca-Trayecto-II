from config.conexion import Conexion
import psycopg2.extras

class Modelo_cliente(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, nombre, apellido, cedula, telefono, direccion, correo):
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
        except Exception as e:
            print(f"Error en Modelo_cliente.Insert: {e}")
            return 0 # Devuelve 0 para indicar que no se insertaron filas
        finally:
            if cursor:
                cursor.close()
    
    # ESTE ES EL QUE SE USA
    def Select_por_cedula(self, cedula):
        cursor = None
        try:
            cursor = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            sql = "SELECT * FROM clientes WHERE cedula = %s LIMIT 1"
            cursor.execute(sql, (cedula,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error en Modelo_cliente.Select_por_cedula: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def Select_por_id(self, id_cliente):
        cursor = None
        try:
            cursor = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            sql = "SELECT * FROM clientes WHERE id_cliente = %s LIMIT 1"
            cursor.execute(sql, (id_cliente,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error en Modelo_cliente.Select_id: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


    def existe_cedula(self, cedula: str) -> bool:
        sql = "SELECT 1 FROM clientes WHERE cedula = %s LIMIT 1"
        cursor = self.con.cursor()
        cursor.execute(sql, (cedula,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado is not None



    def Select_all(self):
        cursor = None
        try:
            cursor = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            sql = "SELECT * FROM clientes"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en Modelo_cliente.Select_all: {e}")
            return []
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
        except Exception as e:
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
        except Exception as e:
            print(f"Error en Modelo_cliente.Delete_por_cedula: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()