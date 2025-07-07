# Archivo: controller/controller_compra.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_compra import Modelo_compra
from model.model_inventario import Modelo_inventario
from model.model_cliente import Modelo_cliente
try:
    from utilis.generador_factura import GeneradorFactura
except ImportError:
    GeneradorFactura = None

class Controlador_compra:
    def __init__(self):
        self.modelo = Modelo_compra()
        self.modelo_inventario = Modelo_inventario()
        self.modelo_cliente = Modelo_cliente()

    def registrar_compra(self, id_cliente, id_inventario, cantidad, fecha, total):
        # La lógica de registrar es más simple y puede que no necesite transacción explícita si es solo un INSERT y un UPDATE.
        # Pero para ser consistentes, también la envolvemos en una transacción.
        self.modelo_inventario.iniciar_transaccion()
        try:
            # Verificar stock
            stock_actual = self.modelo_inventario.obtener_stock_actual(id_inventario)
            if stock_actual is None or stock_actual < cantidad:
                self.modelo_inventario.revertir_transaccion()
                return 0
            
            # Insertar compra
            id_nueva_compra = self.modelo.Insert(id_cliente, id_inventario, cantidad, fecha, total)
            if not id_nueva_compra:
                self.modelo_inventario.revertir_transaccion()
                return 0

            # Actualizar stock
            self.modelo_inventario.actualizar_stock(id_inventario, -cantidad)
            
            self.modelo_inventario.confirmar_transaccion()
            return id_nueva_compra
        except Exception as e:
            print(f"Error al registrar compra: {e}")
            self.modelo_inventario.revertir_transaccion()
            return 0

    def obtener_todas_las_compras(self):
        return self.modelo.Select_all()

    def actualizar_compra(self, id_compra, id_cliente, id_inventario_nuevo, cantidad_nueva, fecha, total):
        # <<<<<<<<<<<<<<<<<<<< LÓGICA DE ACTUALIZACIÓN DE STOCK COMPLETAMENTE CORREGIDA >>>>>>>>>>>>>>>>>>>>
        compra_original = self.modelo.Select_por_id_simple(id_compra)
        if not compra_original:
            print(f"Error: No se encontró la compra original con ID {id_compra}")
            return False
        
        id_inventario_viejo, cantidad_vieja = compra_original

        # Iniciar la transacción aquí, al principio de toda la operación.
        self.modelo_inventario.iniciar_transaccion()
        try:
            # CASO 1: El producto es el MISMO, solo cambia la cantidad.
            if id_inventario_nuevo == id_inventario_viejo:
                # Calculamos cuántas unidades hay que devolver o quitar del stock.
                # ej: viejo=5, nuevo=7 -> diferencia=-2 (quitar 2 más)
                # ej: viejo=5, nuevo=3 -> diferencia=2 (devolver 2)
                diferencia_stock = cantidad_vieja - cantidad_nueva
                
                stock_actual = self.modelo_inventario.obtener_stock_actual(id_inventario_nuevo)
                
                # Verificamos si hay suficiente stock para el cambio.
                if stock_actual < -diferencia_stock: # ej: stock=10, diferencia=-2, 10 < 2 (Falso)
                    raise Exception("Stock insuficiente para el nuevo producto.")
                
                self.modelo_inventario.actualizar_stock(id_inventario_nuevo, diferencia_stock)

            # CASO 2: Se cambia de un producto a OTRO.
            else:
                # 1. Devolvemos el stock del producto viejo.
                self.modelo_inventario.actualizar_stock(id_inventario_viejo, cantidad_vieja)
                
                # 2. Verificamos si hay suficiente stock del producto nuevo.
                stock_nuevo = self.modelo_inventario.obtener_stock_actual(id_inventario_nuevo)
                if stock_nuevo < cantidad_nueva:
                    raise Exception("Stock insuficiente para el nuevo producto.")
                    
                # 3. Descontamos el stock del nuevo producto.
                self.modelo_inventario.actualizar_stock(id_inventario_nuevo, -cantidad_nueva)
            
            # 4. Si todo el manejo de stock fue exitoso, actualizamos el registro de la compra.
            resultado_update = self.modelo.Update(id_compra, id_cliente, id_inventario_nuevo, cantidad_nueva, fecha, total)
            if not resultado_update:
                raise Exception("Falló la actualización del registro de la compra.")

            # 5. Si todo salió bien, confirmamos la transacción.
            self.modelo_inventario.confirmar_transaccion()
            return True

        except Exception as e:
            print(f"Error al actualizar compra: {e}")
            self.modelo_inventario.revertir_transaccion()
            return False
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FIN DE LA LÓGICA CORREGIDA >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def eliminar_compra(self, id_compra):
        compra_a_eliminar = self.modelo.Select_por_id_simple(id_compra)
        if not compra_a_eliminar: return False

        id_inventario, cantidad = compra_a_eliminar
        
        self.modelo_inventario.iniciar_transaccion()
        try:
            self.modelo_inventario.actualizar_stock(id_inventario, cantidad)
            self.modelo.Delete(id_compra)
            self.modelo_inventario.confirmar_transaccion()
            return True
        except Exception as e:
            print(f"Error al eliminar compra: {e}")
            self.modelo_inventario.revertir_transaccion()
            return False
    
    # ... (el resto del código de generar factura está bien) ...
    
    def generar_factura_venta(self, id_compra):
        if GeneradorFactura is None: return None, "Módulo de facturas no disponible."
        
        datos_venta_raw = self.modelo.Select_por_id_completo(id_compra)
        if not datos_venta_raw: return None, "No se encontraron los datos de la venta."

        datos_cliente_raw = self.modelo_cliente.Select_por_id(datos_venta_raw['id_cliente'])
        if not datos_cliente_raw: return None, "No se encontraron los datos del cliente."

        datos_venta = {
            'id_compra': datos_venta_raw['id_compra'],
            'fecha': datos_venta_raw['fecha'].strftime('%d/%m/%Y'),
            'producto': datos_venta_raw['nombre_producto'],
            'cantidad': datos_venta_raw['cantidad'],
            'total': float(datos_venta_raw['total'])
        }
        
        datos_cliente = {
            'nombre_completo': datos_cliente_raw['nombre_completo'],
            'cedula': datos_cliente_raw['cedula']
        }
        
        try:
            generador = GeneradorFactura(datos_venta, datos_cliente)
            path_pdf = generador.generar_pdf()
            return path_pdf, "Factura generada exitosamente."
        except Exception as e:
            return None, f"Error al generar el PDF: {e}"