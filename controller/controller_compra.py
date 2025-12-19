import os
import sys
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.model_compra import Modelo_compra
from model.model_inventario import Modelo_inventario
from model.model_cliente import Modelo_cliente

try:
    from utils.generador_factura import GeneradorFactura
except ImportError:
    GeneradorFactura = None


class Controlador_compra:
    def __init__(self):
        self.modelo_compra = Modelo_compra()
        self.modelo_inventario = Modelo_inventario()
        self.modelo_cliente = Modelo_cliente()

    def registrar_compra_completa(self, id_cliente, items_carrito):
        """
        Orquesta el registro completo de una compra (transacción).
        """
        con = None
        cursor = None

        try:
            con = self.modelo_compra.get_conexion()
            cursor = con.cursor()

            # Calcular total general
            total_general = sum(item['subtotal'] for item in items_carrito)

            # Inserta compra maestra
            id_nueva_compra = self.modelo_compra.insertar_compra_maestra(
                cursor, id_cliente, total_general
            )

            if not id_nueva_compra:
                raise Exception("No se pudo crear la compra.")

            # Inserta detalles + descuenta stock
            for item in items_carrito:
                self.modelo_compra.insertar_detalle_compra(
                    cursor,
                    id_compra=id_nueva_compra,
                    id_inventario=item['id_inventario'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario']
                )

                cursor.execute(
                    """
                    UPDATE inventario
                    SET cantidad_actual = cantidad_actual - %s
                    WHERE id_inventario = %s
                    """,
                    (item['cantidad'], item['id_inventario'])
                )

            # Commit de la transacción
            con.commit()
            return id_nueva_compra

        except psycopg2.Error as e:
            if con:
                con.rollback()
            print(f"ERROR en la transacción de compra: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    def obtener_todas_las_compras(self):
        """
        Retorna todas las compras con sus detalles.
        """
        return self.modelo_compra.Select_all()

    def generar_factura_compra(self, id_compra):
        """
        Genera un PDF de factura de compra.
        """
        if GeneradorFactura is None:
            return None, "Módulo de facturas no disponible."

        datos_compra, detalles_compra = self.modelo_compra.Select_compra_completa_para_factura(id_compra)

        if not datos_compra or not detalles_compra:
            return None, "No se encontraron los datos de la compra."

        datos_cliente = self.modelo_cliente.Select_por_id(datos_compra['id_cliente'])

        if not datos_cliente:
            return None, "No se encontraron los datos del cliente."

        datos_factura = {
            'id_compra': datos_compra['id_compra'],
            'fecha': datos_compra['fecha'].strftime('%d/%m/%Y %H:%M:%S'),
            'total': float(datos_compra['total']),
            'items': detalles_compra
        }

        datos_cliente_factura = {
            'nombre_completo': f"{datos_cliente['nombre']} {datos_cliente['apellido']}",
            'cedula': datos_cliente['cedula']
        }

        try:
            generador = GeneradorFactura(datos_factura, datos_cliente_factura)
            path_pdf = generador.generar_pdf()
            return path_pdf, "Factura generada exitosamente."
        except Exception as e:
            return None, f"Error al generar el PDF: {e}"
