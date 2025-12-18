# Archivo: model/model_cierre_caja.py (CORREGIDO)
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_cierre_caja(Conexion):
    def __init__(self):
        super().__init__()

    def abrir_caja(self, monto_inicial):
        con = self.get_conexion()
        cursor = None
        try:
            cursor = con.cursor()
            sql = "INSERT INTO cierres_caja (fecha_apertura, monto_inicial, estado) VALUES (NOW(), %s, 'ABIERTA')"
            cursor.execute(sql, (monto_inicial,))
            con.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al abrir caja: {e}")
            return 0
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()

    def obtener_sesion_abierta(self):
        con = self.get_conexion()
        cursor = None
        try:
            cursor = con.cursor(dictionary=True)
            sql = "SELECT * FROM cierres_caja WHERE estado = 'ABIERTA' LIMIT 1"
            cursor.execute(sql)
            return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener sesión abierta: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()

    def calcular_ventas_del_periodo(self, fecha_apertura):
        """
        Suma el total de todas las ventas realizadas desde la apertura de caja.
        """
        con = self.get_conexion()
        cursor = None
        try:
            cursor = con.cursor()
            # <<<<<<<<<<<<<<<<< ESTA ES LA CONSULTA SQL CORREGIDA Y DEFINITIVA >>>>>>>>>>>>>>>>>
            # Se asegura de sumar la columna 'total_venta' de la tabla 'ventas', filtrando
            # por 'fecha_venta'. Esto ahora coincide con donde se guardan las ventas.
            sql = "SELECT SUM(total_venta) FROM ventas WHERE fecha_venta >= %s"
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            
            # --- Para Depuración (puedes descomentar estas líneas si el error persiste) ---
            # print(f"DEBUG: Calculando ventas desde: {fecha_apertura}")
            cursor.execute(sql, (fecha_apertura,))
            resultado = cursor.fetchone()[0]
            # print(f"DEBUG: Resultado de SUM(total_venta) es: {resultado}")
            # --------------------------------------------------------------------------

            return resultado if resultado is not None else 0.00
        except Error as e:
            print(f"Error al calcular ventas del periodo: {e}")
            return 0.00
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()

    def cerrar_caja(self, id_cierre, ventas_sistema, monto_final, diferencia, observaciones):
        con = self.get_conexion()
        cursor = None
        try:
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
            valores = (ventas_sistema, monto_final, diferencia, observaciones, id_cierre)
            cursor.execute(sql, valores)
            con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al cerrar caja: {e}")
            return 0
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()