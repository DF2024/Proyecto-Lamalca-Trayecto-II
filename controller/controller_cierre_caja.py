# Archivo: controller/controller_cierre_caja.py
import os
import sys
from decimal import Decimal, InvalidOperation # <<-- IMPORTANTE: Importar Decimal

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
        sesion_abierta = self.modelo.obtener_sesion_abierta()
        if not sesion_abierta:
            return None
        
        ventas_periodo = self.modelo.calcular_ventas_del_periodo(sesion_abierta['fecha_apertura'])
        
        # Aseguramos que todo sea Decimal para la vista
        monto_inicial_decimal = Decimal(sesion_abierta['monto_inicial'])
        ventas_decimal = Decimal(ventas_periodo)

        datos_cierre = {
            "id_cierre": sesion_abierta['id_cierre'],
            "monto_inicial": monto_inicial_decimal,
            "ventas_sistema": ventas_decimal,
            "total_esperado": monto_inicial_decimal + ventas_decimal
        }
        return datos_cierre

    def finalizar_cierre(self, id_cierre, ventas_sistema, monto_final_contado_float, observaciones):
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<< ESTA ES LA CORRECCIÓN CLAVE >>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            # 1. Obtenemos el total esperado (que ya es Decimal)
            sesion_abierta = self.modelo.obtener_sesion_abierta()
            if not sesion_abierta:
                return False 

            total_esperado = Decimal(sesion_abierta['monto_inicial']) + Decimal(ventas_sistema)
            
            # 2. Convertimos el monto contado (que viene como float desde la vista) a Decimal
            #    Se convierte a string primero para evitar problemas de precisión de float
            monto_final_decimal = Decimal(str(monto_final_contado_float))

            # 3. Ahora la resta es entre dos objetos Decimal, lo cual es seguro.
            diferencia = monto_final_decimal - total_esperado
        
        except (InvalidOperation, TypeError):
            # En caso de que la conversión o el cálculo falle
            return False

        # 4. Pasamos los objetos Decimal al modelo.
        return self.modelo.cerrar_caja(id_cierre, ventas_sistema, monto_final_decimal, diferencia, observaciones)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<