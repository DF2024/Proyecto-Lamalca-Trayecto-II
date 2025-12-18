import os
import sys
from mysql.connector import Error

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
        self.modelo_compra = Modelo_compra()
        self.modelo_inventario = Modelo_inventario()
        self.modelo_cliente = Modelo_cliente()

    def registrar_venta_completa(self, id_cliente, items_carrito):
        """
        Orquesta el registro de una venta. Ya no recibe la fecha.
        """
        con = self.modelo_compra.get_conexion()
        if not con or not con.is_connected():
            print("Error: No se pudo establecer conexión para la transacción.")
            return None
        
        cursor = None
        try:
            cursor = con.cursor()
            con.start_transaction()

            total_general = sum(item['subtotal'] for item in items_carrito)
            
            # Llamada al modelo corregida: sin fecha.
            id_nueva_venta = self.modelo_compra.insertar_venta_maestra(cursor, id_cliente, total_general)

            if not id_nueva_venta:
                raise Exception("Fallo al crear el registro maestro de la venta.")

            for item in items_carrito:
                self.modelo_compra.insertar_detalle_venta(
                    cursor,
                    id_venta=id_nueva_venta,
                    id_inventario=item['id_inventario'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario']
                )
                sql_stock = "UPDATE inventario SET cantidad_actual = cantidad_actual - %s WHERE id_inventario = %s"
                cursor.execute(sql_stock, (item['cantidad'], item['id_inventario']))

            con.commit()
            return id_nueva_venta

        except Error as e:
            print(f"ERROR en la transacción de venta. Revirtiendo... Error: {e}")
            if con:
                con.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if con and con.is_connected():
                con.close()

    def obtener_todas_las_compras(self):
        return self.modelo_compra.Select_all()

    def generar_factura_venta(self, id_venta):
        if GeneradorFactura is None:
            return None, "Módulo de facturas no disponible."
            
        datos_venta, detalles_venta = self.modelo_compra.Select_venta_completa_para_factura(id_venta)
        if not datos_venta or not detalles_venta:
            return None, "No se encontraron los datos de la venta."

        datos_cliente_raw = self.modelo_cliente.Select_por_id(datos_venta['id_cliente'])
        if not datos_cliente_raw:
            return None, "No se encontraron los datos del cliente."
        
        datos_factura = {
            'id_venta': datos_venta['id_venta'],
            'fecha': datos_venta['fecha_venta'].strftime('%d/%m/%Y %H:%M:%S'),
            'total': float(datos_venta['total_venta']),
            'items': detalles_venta
        }
        
        datos_cliente = {
            'nombre_completo': datos_cliente_raw['nombre_completo'],
            'cedula': datos_cliente_raw['cedula']
        }
        
        try:
            generador = GeneradorFactura(datos_factura, datos_cliente)
            path_pdf = generador.generar_pdf()
            return path_pdf, "Factura generada exitosamente."
        except Exception as e:
            return None, f"Error al generar el PDF: {e}"