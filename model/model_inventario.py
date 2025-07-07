# Archivo: model/model_inventario.py
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_inventario(Conexion):
    def __init__(self):
        super().__init__()
        # <<-- MEJORADO: La conexión se obtiene solo cuando se necesita, no en el init -->>

    # --- Métodos de gestión de transacciones ---
    def iniciar_transaccion(self):
        try:
            self.con = self.get_conexion()
            self.con.start_transaction()
            print("[TRANSACCIÓN INVENTARIO] Iniciada.")
        except Error as e:
            print(f"Error al iniciar transacción: {e}")
            self.con = None

    def confirmar_transaccion(self):
        if self.con and self.con.is_connected():
            self.con.commit()
            print("[TRANSACCIÓN INVENTARIO] Confirmada (Commit).")
            self.con.close()

    def revertir_transaccion(self):
        if self.con and self.con.is_connected():
            self.con.rollback()
            print("[TRANSACCIÓN INVENTARIO] Revertida (Rollback).")
            self.con.close()

    # --- Operaciones de datos ---
    def obtener_stock_actual(self, id_inventario):
        """Obtiene el stock actual de un producto, usando la conexión de la transacción actual."""
        if not self.con or not self.con.is_connected():
            print("Error: No hay conexión de transacción activa para obtener stock.")
            return None
        
        cursor = None
        try:
            # `FOR UPDATE` bloquea la fila para que nadie más la pueda leer o modificar hasta que termine la transacción.
            # Esto evita "race conditions" y bloqueos.
            sql = "SELECT cantidad_actual FROM inventario WHERE id_inventario = %s FOR UPDATE"
            cursor = self.con.cursor()
            cursor.execute(sql, (id_inventario,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Error as e:
            print(f"Error al obtener stock actual: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def actualizar_stock(self, id_inventario, cambio_cantidad):
        """Actualiza el stock. Debe ser llamado dentro de una transacción iniciada."""
        if not self.con or not self.con.is_connected():
            print("Error: No hay conexión de transacción activa para actualizar stock.")
            return False
            
        print(f"[STOCK] Preparado cambio para id {id_inventario}: {cambio_cantidad}")
        cursor = None
        try:
            sql = "UPDATE inventario SET cantidad_actual = cantidad_actual + (%s) WHERE id_inventario = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (cambio_cantidad, id_inventario))
            return True
        except Error as e:
            # No imprimimos el error aquí, se capturará en el controlador que maneja la transacción.
            raise e # <<-- Re-lanzamos la excepción para que el controlador la capture y haga rollback.
        finally:
            if cursor:
                cursor.close()

    # Mantenemos las funciones originales por si se usan en otras partes, pero las de transacción son preferibles.
    def Insert(self, *args): pass
    def Select_all(self):
        con = self.get_conexion()
        cursor = con.cursor()
        sql = "SELECT *, 10.0 AS precio_venta FROM inventario" # Añadido precio_venta para compatibilidad
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()
        con.close()
        return resultado
    def Update(self, *args): pass
    def Delete(self, *args): pass