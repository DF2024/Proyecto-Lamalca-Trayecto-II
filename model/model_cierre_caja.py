# Archivo: model/model_cierre_caja.py (POSTGRESQL FINAL)

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.conexion import Conexion
import psycopg2
from psycopg2.extras import RealDictCursor


class Modelo_cierre_caja(Conexion):
    def __init__(self):
        super().__init__()

    def abrir_caja(self, monto_inicial):
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor()

            sql = """
                INSERT INTO cierres_caja (fecha_apertura, monto_inicial, estado)
                VALUES (NOW(), %s, 'ABIERTA')
                RETURNING id_cierre;
            """
            cursor.execute(sql, (monto_inicial,))
            id_cierre = cursor.fetchone()[0]

            con.commit()
            return id_cierre

        except psycopg2.Error as e:
            if con:
                con.rollback()
            print(f"Error al abrir caja: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    def obtener_sesion_abierta(self):
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor(cursor_factory=RealDictCursor)

            sql = """
                SELECT *
                FROM cierres_caja
                WHERE estado = 'ABIERTA'
                ORDER BY fecha_apertura DESC
                LIMIT 1
            """
            cursor.execute(sql)
            return cursor.fetchone()

        except psycopg2.Error as e:
            print(f"Error al obtener sesión abierta: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    def calcular_ventas_del_periodo(self, fecha_apertura):
        """
        Suma el total de ventas realizadas desde la apertura de caja.
        """
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor()

            sql = """
                SELECT COALESCE(SUM(total), 0)
                FROM compras
                WHERE fecha >= %s
            """
            cursor.execute(sql, (fecha_apertura,))
            return cursor.fetchone()[0]

        except psycopg2.Error as e:
            print(f"Error al calcular ventas del periodo: {e}")
            return 0

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    def cerrar_caja(self, id_cierre, ventas_sistema, monto_final, diferencia, observaciones):
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor()

            sql = """
                UPDATE cierres_caja
                SET fecha_cierre = NOW(),
                    ventas_sistema = %s,
                    monto_final_contado = %s,
                    diferencia = %s,
                    observaciones = %s,
                    estado = 'CERRADA'
                WHERE id_cierre = %s
            """
            cursor.execute(sql, (
                ventas_sistema,
                monto_final,
                diferencia,
                observaciones,
                id_cierre
            ))

            con.commit()
            return cursor.rowcount

        except psycopg2.Error as e:
            if con:
                con.rollback()
            print(f"Error al cerrar caja: {e}")
            return 0

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()
