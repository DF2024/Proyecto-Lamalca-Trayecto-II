import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_compra import Modelo_compra
from model.model_inventario import Modelo_inventario
from model.model_cliente import Modelo_cliente 
from utilis.generador_factura import GeneradorFactura 

class Controlador_compra:
    def __init__(self):
        self.modelo = Modelo_compra()
        self.modelo_inventario = Modelo_inventario()
        self.modelo_cliente = Modelo_cliente()

    def registrar_compra(self, id_cliente, id_inventario, cantidad, fecha, total):
        id_nueva_compra = self.modelo.Insert(id_cliente, id_inventario, cantidad, fecha, total)
        if id_nueva_compra:
            self.modelo_inventario.actualizar_stock(id_inventario, -cantidad)
        return id_nueva_compra

    def generar_factura_venta(self, id_compra):
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

    def obtener_todas_las_compras(self):
        return self.modelo.Select_all()

    def actualizar_compra(self, id_compra, id_cliente, id_inventario_nuevo, cantidad_nueva, fecha, total):
        # Lógica de actualización de stock:
        # 1. Obtener los datos de la compra original (producto y cantidad viejos)
        compra_original = self.modelo.Select_por_id(id_compra)
        if not compra_original: return False
        
        id_inventario_viejo, cantidad_vieja = compra_original

        # 2. Devolver el stock del producto original
        self.modelo_inventario.actualizar_stock(id_inventario_viejo, cantidad_vieja)

        # 3. Descontar el stock del nuevo producto
        self.modelo_inventario.actualizar_stock(id_inventario_nuevo, -cantidad_nueva)
        
        # 4. Actualizar el registro de la compra
        return self.modelo.Update(id_compra, id_cliente, id_inventario_nuevo, cantidad_nueva, fecha, total)

    def eliminar_compra(self, id_compra):
        # 1. Antes de eliminar, necesitamos saber qué producto y cantidad devolver al stock
        compra_a_eliminar = self.modelo.Select_por_id(id_compra)
        if not compra_a_eliminar: return False

        id_inventario, cantidad = compra_a_eliminar
        
        # 2. Devolvemos la cantidad al inventario
        self.modelo_inventario.actualizar_stock(id_inventario, cantidad)

        # 3. Ahora sí, eliminamos el registro de la compra
        return self.modelo.Delete(id_compra)
    
    # <<-- NUEVA FUNCIÓN PARA GENERAR LA FACTURA -->>
    def generar_factura_venta(self, id_compra):
        """
        Orquesta la creación de un PDF para una venta específica.
        """
        # 1. Obtener los datos completos de la venta
        datos_venta_raw = self.modelo.Select_por_id_completo(id_compra) # Necesitaremos crear esta función
        if not datos_venta_raw:
            return None, "No se encontraron los datos de la venta."

        # 2. Obtener los datos completos del cliente
        id_cliente = datos_venta_raw['id_cliente']
        datos_cliente_raw = self.modelo_cliente.Select_por_id(id_cliente) # Necesitaremos esta función
        if not datos_cliente_raw:
            return None, "No se encontraron los datos del cliente."

        # 3. Formatear los datos para el generador de PDF
        datos_venta_limpios = {
            'id_compra': datos_venta_raw['id_compra'],
            'fecha': datos_venta_raw['fecha'].strftime('%d/%m/%Y'),
            'producto': datos_venta_raw['nombre_producto'],
            'cantidad': datos_venta_raw['cantidad'],
            'total': float(datos_venta_raw['total'])
        }
        
        datos_cliente_limpios = {
            'nombre_completo': datos_cliente_raw['nombre_completo'],
            'cedula': datos_cliente_raw['cedula'],
            'telefono': datos_cliente_raw.get('telefono'), # Usamos .get por si es opcional
            'direccion': datos_cliente_raw.get('direccion')
        }
        
        # 4. Llamar al generador de PDF
        try:
            generador = GeneradorFactura(datos_venta_limpios, datos_cliente_limpios)
            path_pdf = generador.generar_pdf()
            return path_pdf, "Factura generada exitosamente."
        except Exception as e:
            return None, f"Error al generar el PDF: {e}"