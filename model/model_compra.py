# Archivo: model/model_compra.py
import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.conexion import Conexion


class Modelo_compra(Conexion):

    def insertar_compra_maestra(self, cursor, id_cliente, total_compra):
        """
        Inserta una compra en la tabla compras y retorna su id.
        """
        sql = """
            INSERT INTO compras (id_cliente, fecha, total)
            VALUES (%s, NOW(), %s)
            RETURNING id_compra;
        """
        cursor.execute(sql, (id_cliente, total_compra))
        return cursor.fetchone()[0]

    def insertar_detalle_compra(self, cursor, id_compra, id_inventario, cantidad, precio_unitario):
        """
        Inserta el detalle de una compra.
        """
        sql = """
            INSERT INTO compras_detalle (
                id_compra, id_inventario, cantidad, precio_unitario
            )
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(sql, (id_compra, id_inventario, cantidad, precio_unitario))

    def Select_all(self):
        """
        Obtiene el historial completo de compras con sus productos.
        """
        con = self.get_conexion()
        cursor = None
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            sql = """
                SELECT 
                    cp.id_compra,
                    c.cedula,
                    CONCAT(c.nombre, ' ', c.apellido) AS nombre_cliente,
                    i.producto AS nombre_producto,
                    cd.cantidad,
                    cp.fecha AS fecha,
                    (cd.cantidad * cd.precio_unitario) AS total_linea
                FROM compras_detalle cd
                JOIN compras cp ON cd.id_compra = cp.id_compra
                JOIN clientes c ON cp.id_cliente = c.id_cliente
                JOIN inventario i ON cd.id_inventario = i.id_inventario
                ORDER BY cp.fecha DESC, cp.id_compra DESC;
            """
            cursor.execute(sql)
            return cursor.fetchall()

        except psycopg2.Error as e:
            print(f"Error al seleccionar compras: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    def Select_compra_completa_para_factura(self, id_compra):
        con = self.get_conexion()
        cursor = None
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM compras WHERE id_compra = %s", (id_compra,))
            datos_compra = cursor.fetchone()
            if not datos_compra:
                return None, None
            sql_detalles = """
                SELECT cd.*, i.producto AS nombre_producto
                FROM compras_detalle cd
                JOIN inventario i ON cd.id_inventario = i.id_inventario
                WHERE cd.id_compra = %s
            """
            cursor.execute(sql_detalles, (id_compra,))
            detalles_compra = cursor.fetchall()
            return datos_compra, detalles_compra
        except Exception as e:
            print(f"Error al obtener datos completos de la compra: {e}")
            return None, None
        finally:
            if cursor: cursor.close()
            if con: con.close()