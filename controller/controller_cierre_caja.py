# Archivo: controller/controller_cierre_caja.py (VERSIÓN FINAL Y SIMPLIFICADA)
import os
import sys
from decimal import Decimal, InvalidOperation

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_cierre_caja import Modelo_cierre_caja

class Controlador_cierre_caja:
    def __init__(self):
        self.modelo = Modelo_cierre_caja()

    def iniciar_caja(self, monto_inicial):
        sesion_existente = self.modelo.obtener_sesion_abierta()
        if sesion_existente:
            return "Error: Ya hay una caja abierta."
        
        resultado = self.modelo.abrir_caja(monto_inicial)
        return resultado > 0

    def obtener_estado_caja(self):
        return self.modelo.obtener_sesion_abierta()

    def preparar_datos_cierre(self):
        """
        Esta es la ÚNICA función que consulta y calcula los datos del periodo.
        Devuelve todo lo necesario para la vista y para el cierre final.
        """
        sesion_abierta = self.modelo.obtener_sesion_abierta()
        if not sesion_abierta:
            return None
        
        # Esta consulta ahora es confiable gracias a los arreglos en el módulo de compras.
        ventas_periodo = self.modelo.calcular_ventas_del_periodo(sesion_abierta['fecha_apertura'])
        
        monto_inicial_decimal = Decimal(sesion_abierta['monto_inicial'])
        ventas_decimal = Decimal(ventas_periodo)
        total_esperado_decimal = monto_inicial_decimal + ventas_decimal

        datos_cierre = {
            "id_cierre": sesion_abierta['id_cierre'],
            "monto_inicial": monto_inicial_decimal,
            "ventas_sistema": ventas_decimal,
            "total_esperado": total_esperado_decimal
        }
        return datos_cierre

    def finalizar_cierre(self, id_cierre, ventas_sistema, monto_final_contado_float, observaciones):
        """
        Esta función ahora es más simple. Confía en los datos que la vista
        obtuvo (y que se actualizan con el foco) y calcula la diferencia final.
        """
        try:
            # Convierte los datos recibidos a Decimal para el cálculo final
            ventas_sistema_decimal = Decimal(ventas_sistema)
            monto_final_decimal = Decimal(str(monto_final_contado_float))
            
            # Para calcular la diferencia, necesitamos el total esperado que se basa
            # en el monto inicial y las ventas del sistema.
            sesion_abierta = self.modelo.obtener_sesion_abierta()
            if not sesion_abierta: return False
            monto_inicial_decimal = Decimal(sesion_abierta['monto_inicial'])

            total_esperado = monto_inicial_decimal + ventas_sistema_decimal
            diferencia = monto_final_decimal - total_esperado
        
        except (InvalidOperation, TypeError) as e:
            print(f"Error de cálculo en finalizar_cierre: {e}")
            return False

        # Pasa todos los datos al modelo para ser guardados.
        return self.modelo.cerrar_caja(id_cierre, ventas_sistema_decimal, monto_final_decimal, diferencia, observaciones)