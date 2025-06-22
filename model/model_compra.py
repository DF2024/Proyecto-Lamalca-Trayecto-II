# model/model_compra.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_compra(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()
        # No es necesario inicializar self.cursor aquí si lo creamos en cada método

    def Insert(self, id_cliente, id_producto, cantidad, fecha, total):
        cursor = None  # Definir fuera del try para que exista en el finally
        try:
            cursor = self.con.cursor() # Se crea el cursor local
            sql = '''
                INSERT INTO compras (id_cliente, id_producto, cantidad, fecha, total)
                VALUES (%s, %s, %s, %s, %s)
            '''
            # CORRECCIÓN: Se usa la variable local 'cursor', no 'self.cursor'
            cursor.execute(sql, (id_cliente, id_producto, cantidad, fecha, total))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al insertar compra: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Select_all(self):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = """
                SELECT 
                    co.id_compra, cl.cedula, CONCAT(cl.nombre, ' ', cl.apellido) AS nombre_cliente,
                    p.nombre AS nombre_producto, co.cantidad, co.fecha, co.total,
                    co.id_cliente, co.id_producto
                FROM compras AS co
                JOIN clientes AS cl ON co.id_cliente = cl.id_cliente
                JOIN productos AS p ON co.id_producto = p.id_producto
                ORDER BY co.fecha DESC, co.id_compra DESC
            """
            # CORRECCIÓN: Se usa la variable local 'cursor'
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al seleccionar todas las compras: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def Update(self, id_compra, id_cliente, id_producto, cantidad, fecha, total):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = '''
                UPDATE compras
                SET id_cliente = %s, id_producto = %s, cantidad = %s, fecha = %s, total = %s
                WHERE id_compra = %s
            '''
            valores = (id_cliente, id_producto, cantidad, fecha, total, id_compra)
            # CORRECCIÓN: Se usa la variable local 'cursor'
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al actualizar compra: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Delete(self, id_compra):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "DELETE FROM compras WHERE id_compra = %s"
            # CORRECCIÓN: Se usa la variable local 'cursor'
            cursor.execute(sql, (id_compra,))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al eliminar compra: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            
    def __del__(self):
        if self.con and self.con.is_connected():
            self.con.close()