# Archivo: model/model_compra.py (VERSIÓN FINAL Y VERIFICADA)
import os
import sys
from mysql.connector import Error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion

class Modelo_compra(Conexion):
    def __init__(self):
        super().__init__()

    def insertar_venta_maestra(self, cursor, id_cliente, total_venta):
        """
        Inserta un registro en la tabla maestra 'ventas' usando NOW() para la fecha.
        """
        sql = "INSERT INTO ventas (id_cliente, fecha_venta, total_venta) VALUES (%s, NOW(), %s)"
        cursor.execute(sql, (id_cliente, total_venta))
        return cursor.lastrowid

    def insertar_detalle_venta(self, cursor, id_venta, id_inventario, cantidad, precio_unitario):
        """
        Inserta un producto en la tabla 'ventas_detalle'.
        """
        sql = "INSERT INTO ventas_detalle (id_venta, id_inventario, cantidad, precio_unitario_venta) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_venta, id_inventario, cantidad, precio_unitario))

    def Select_all(self):
        """
        Obtiene el historial de ítems individuales vendidos desde la nueva estructura de tablas.
        """
        con = self.get_conexion()
        cursor = None
        try:
            cursor = con.cursor(dictionary=True)
            sql = """
                SELECT 
                    v.id_venta,
                    c.cedula,
                    CONCAT(c.nombre, ' ', c.apellido) AS nombre_cliente,
                    i.producto AS nombre_producto,
                    vd.cantidad,
                    v.fecha_venta AS fecha,
                    (vd.cantidad * vd.precio_unitario_venta) AS total_linea,
                    v.id_cliente,
                    vd.id_inventario
                FROM ventas_detalle vd
                JOIN ventas v ON vd.id_venta = v.id_venta
                JOIN clientes c ON v.id_cliente = c.id_cliente
                JOIN inventario i ON vd.id_inventario = i.id_inventario
                ORDER BY v.fecha_venta DESC, v.id_venta DESC;
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al seleccionar todas las compras: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()
            
    def Select_venta_completa_para_factura(self, id_venta):
        """
        Obtiene todos los datos de una venta y sus detalles para generar una factura.
        """
        con = self.get_conexion()
        cursor = None
        try:
            cursor = con.cursor(dictionary=True)
            sql_venta = "SELECT * FROM ventas WHERE id_venta = %s"
            cursor.execute(sql_venta, (id_venta,))
            datos_venta = cursor.fetchone()

            if not datos_venta:
                return None, None

            sql_detalles = """
                SELECT vd.*, i.producto as nombre_producto 
                FROM ventas_detalle vd
                JOIN inventario i ON vd.id_inventario = i.id_inventario
                WHERE vd.id_venta = %s
            """
            cursor.execute(sql_detalles, (id_venta,))
            detalles_venta = cursor.fetchall()
            
            return datos_venta, detalles_venta
        except Error as e:
            print(f"Error al obtener datos completos de la venta: {e}")
            return None, None
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()