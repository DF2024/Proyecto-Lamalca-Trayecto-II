# Archivo: utilis/generador_factura.py (ACTUALIZADO)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
import os
from decimal import Decimal, ROUND_HALF_UP

class GeneradorFactura:
    TASA_IVA = Decimal('0.16')

    def __init__(self, datos_venta, datos_cliente, nombre_empresa="Tu Ferretería La Malca", rif_empresa="J-12345678-9"):
        self.datos_venta = datos_venta
        self.datos_cliente = datos_cliente
        self.nombre_empresa = nombre_empresa
        self.rif_empresa = rif_empresa
        
        # El ID ahora viene de 'id_venta'
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.nombre_archivo = f"factura_{self.datos_venta['id_compra']}_{timestamp}.pdf"
        
        self._calcular_impuestos()

    def _calcular_impuestos(self):
        # El total ya viene calculado, lo usamos para desglosar el IVA
        total_venta = Decimal(str(self.datos_venta['total']))
        centavos = Decimal('0.01')
        self.costo_bruto = (total_venta / (1 + self.TASA_IVA)).quantize(centavos, ROUND_HALF_UP)
        self.monto_iva = (total_venta - self.costo_bruto).quantize(centavos, ROUND_HALF_UP)

    def generar_pdf(self):
        directorio_facturas = "facturas"
        if not os.path.exists(directorio_facturas):
            os.makedirs(directorio_facturas)
        
        path_completo = os.path.join(directorio_facturas, self.nombre_archivo)
        
        c = canvas.Canvas(path_completo, pagesize=letter)
        ancho, alto = letter

        margen = inch
        x_izquierda = margen
        x_derecha = ancho - margen
        
        y_actual = alto - margen
        c.setFont("Helvetica-Bold", 18)
        c.drawString(x_izquierda, y_actual, self.nombre_empresa)
        c.setFont("Helvetica", 10)
        c.drawString(x_izquierda, y_actual - 0.2 * inch, f"RIF: {self.rif_empresa}")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(x_derecha, y_actual, "FACTURA")
        c.setFont("Helvetica", 10)
        # Usamos el id_venta del diccionario
        c.drawRightString(x_derecha, y_actual - 0.20 * inch, f"N°: {self.datos_venta['id_compra']:06d}")
        c.drawRightString(x_derecha, y_actual - 0.35 * inch, f"Fecha: {self.datos_venta['fecha']}")
        
        y_actual -= inch

        c.setFont("Helvetica-Bold", 11)
        c.drawString(x_izquierda, y_actual, "Facturar a:")
        y_actual -= 0.25 * inch
        c.setFont("Helvetica", 10)
        c.drawString(x_izquierda, y_actual, f"Nombre: {self.datos_cliente['nombre_completo']}")
        y_actual -= 0.2 * inch
        c.drawString(x_izquierda, y_actual, f"Cédula/RIF: {self.datos_cliente['cedula']}")
        y_actual -= 0.5 * inch

        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.line(x_izquierda, y_actual, x_derecha, y_actual)
        y_actual -= 0.25 * inch
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_izquierda, y_actual, "Descripción")
        c.drawRightString(x_derecha - 3 * inch, y_actual, "Cant.")
        c.drawRightString(x_derecha - 1.5 * inch, y_actual, "Precio Unit.")
        c.drawRightString(x_derecha, y_actual, "Subtotal")
        y_actual -= 0.15 * inch
        c.line(x_izquierda, y_actual, x_derecha, y_actual)
        
        # <<<<<<<<<<<<<<< ESTE ES EL CAMBIO CLAVE: BUCLE PARA LOS PRODUCTOS >>>>>>>>>>>>>>>
        y_actual -= 0.25 * inch
        c.setFont("Helvetica", 10)
        
        # Iteramos sobre la lista de items que nos pasa el controlador
        for item in self.datos_venta['items']:
            cantidad = Decimal(item['cantidad'])
            precio_unitario = Decimal(item['precio_unitario'])
            subtotal_item = cantidad * precio_unitario

            # Desglosamos el IVA por línea para mostrar el precio unitario base
            precio_unitario_base = (precio_unitario / (1 + self.TASA_IVA)).quantize(Decimal('0.01'), ROUND_HALF_UP)
            subtotal_base = (subtotal_item / (1 + self.TASA_IVA)).quantize(Decimal('0.01'), ROUND_HALF_UP)

            c.drawString(x_izquierda, y_actual, item['nombre_producto'])
            c.drawRightString(x_derecha - 3 * inch, y_actual, str(item['cantidad']))
            c.drawRightString(x_derecha - 1.5 * inch, y_actual, f"{precio_unitario_base:.2f}")
            c.drawRightString(x_derecha, y_actual, f"{subtotal_base:.2f}")
            
            y_actual -= 0.25 * inch # Movemos la coordenada Y para el siguiente producto
                                
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FIN DEL CAMBIO CLAVE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        y_actual -= 0.5 * inch
        c.line(x_derecha - 3.5 * inch, y_actual, x_derecha, y_actual)

        y_actual -= 0.2 * inch
        x_etiqueta_total = x_derecha - 2.5 * inch
        x_valor_total = x_derecha
        
        c.setFont("Helvetica", 10)
        c.drawString(x_etiqueta_total, y_actual, "Subtotal:")
        c.drawRightString(x_valor_total, y_actual, f"{self.costo_bruto:.2f} Bs.")
        y_actual -= 0.25 * inch
        
        c.drawString(x_etiqueta_total, y_actual, f"IVA ({int(self.TASA_IVA * 100)}%):")
        c.drawRightString(x_valor_total, y_actual, f"{self.monto_iva:.2f} Bs.")
        y_actual -= 0.1 * inch
        c.line(x_derecha - 3.5 * inch, y_actual, x_derecha, y_actual)
        y_actual -= 0.25 * inch

        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_etiqueta_total, y_actual, "TOTAL A PAGAR:")
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(x_valor_total, y_actual, f"{self.datos_venta['total']:.2f} Bs.")

        y_actual = margen
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(ancho / 2.0, y_actual, "Gracias por su compra.")

        c.save()
        return path_completo