# Archivo: model/model_compra.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_compra(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    # <<-- CORREGIDO: Los nombres de las columnas ahora son id_inventario e id_cliente -->>
    def Insert(self, id_cliente, id_inventario, cantidad, fecha, total):
        cursor = None
        try:
            cursor = self.con.cursor()
            # La tabla compras ahora se relaciona con inventario
            sql = '''
                INSERT INTO compras (id_cliente, id_inventario, cantidad, fecha, total)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (id_cliente, id_inventario, cantidad, fecha, total))
            self.con.commit()
            return cursor.lastrowid  # Devuelve el ID del último registro insertado
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
            # <<-- CORREGIDO: JOIN con la tabla 'inventario' en lugar de 'productos' -->>
            sql = """
                SELECT 
                    co.id_compra, cl.cedula, CONCAT(cl.nombre, ' ', cl.apellido) AS nombre_cliente,
                    inv.producto AS nombre_producto, co.cantidad, co.fecha, co.total,
                    co.id_cliente, co.id_inventario
                FROM compras AS co
                JOIN clientes AS cl ON co.id_cliente = cl.id_cliente
                JOIN inventario AS inv ON co.id_inventario = inv.id_inventario
                ORDER BY co.fecha DESC, co.id_compra DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al seleccionar todas las compras: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    # <<-- NUEVO: Función para obtener una compra específica, útil para devoluciones -->>
    def Select_por_id(self, id_cliente):
        """
        Selecciona un cliente usando su ID primario (id_cliente).
        Devuelve los datos como un diccionario.
        """
        cursor = None
        try:
            cursor = self.con.cursor(dictionary=True)
            # La consulta ahora busca por el ID primario de la tabla
            sql = "SELECT *, CONCAT(nombre, ' ', apellido) as nombre_completo FROM clientes WHERE id_cliente = %s"
            cursor.execute(sql, (id_cliente,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error en Modelo_cliente.Select_por_id: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    # <<-- CORREGIDO: El update también debe referenciar id_inventario -->>
    def Update(self, id_compra, id_cliente, id_inventario, cantidad, fecha, total):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = '''
                UPDATE compras
                SET id_cliente = %s, id_inventario = %s, cantidad = %s, fecha = %s, total = %s
                WHERE id_compra = %s
            '''
            valores = (id_cliente, id_inventario, cantidad, fecha, total, id_compra)
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
            cursor.execute(sql, (id_compra,))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al eliminar compra: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Select_por_id_completo(self, id_compra):
        cursor = None
        try:
            cursor = self.con.cursor(dictionary=True)
            sql = """
                SELECT co.*, inv.producto AS nombre_producto
                FROM compras co
                JOIN inventario inv ON co.id_inventario = inv.id_inventario
                WHERE co.id_compra = %s
            """
            cursor.execute(sql, (id_compra,))
            return cursor.fetchone()
        finally:
            if cursor: cursor.close()

    def __del__(self):
        if self.con and self.con.is_connected():
            self.con.close()