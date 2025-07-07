# Archivo: model/model_cierre_caja.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_cierre_caja(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def abrir_caja(self, monto_inicial):
        cursor = None
        try:
            cursor = self.con.cursor()
            # Inicia una nueva sesión con estado 'ABIERTA'
            sql = "INSERT INTO cierres_caja (fecha_apertura, monto_inicial, estado) VALUES (NOW(), %s, 'ABIERTA')"
            cursor.execute(sql, (monto_inicial,))
            self.con.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al abrir caja: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def obtener_sesion_abierta(self):
        """Busca si hay una sesión de caja actualmente abierta."""
        cursor = None
        try:
            cursor = self.con.cursor(dictionary=True) # Devuelve resultados como diccionarios
            sql = "SELECT * FROM cierres_caja WHERE estado = 'ABIERTA' LIMIT 1"
            cursor.execute(sql)
            return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener sesión abierta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def calcular_ventas_del_periodo(self, fecha_apertura):
        """Suma el total de todas las ventas realizadas desde la apertura de caja."""
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "SELECT SUM(total) FROM compras WHERE fecha >= %s"
            cursor.execute(sql, (fecha_apertura,))
            resultado = cursor.fetchone()[0]
            return resultado if resultado is not None else 0.00
        except Error as e:
            print(f"Error al calcular ventas del periodo: {e}")
            return 0.00
        finally:
            if cursor:
                cursor.close()

    def cerrar_caja(self, id_cierre, ventas_sistema, monto_final, diferencia, observaciones):
        cursor = None
        try:
            cursor = self.con.cursor()
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
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al cerrar caja: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()