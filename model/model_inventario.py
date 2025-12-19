import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from config.conexion import Conexion

class Modelo_inventario(Conexion):
    def __init__(self):
        super().__init__()
        # La conexión se obtiene solo cuando se necesita.

    # --- Operaciones CRUD (Crear, Leer, Actualizar, Borrar) ---
    def Insert(self, producto, cantidad, precio_unitario, fecha_ultima_entrada, categoria, observaciones, proveedor):
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor()
            sql = """INSERT INTO inventario (producto, cantidad_actual, precio_unitario, fecha_ultima_entrada, categoria, observaciones, proveedor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (producto, cantidad, precio_unitario, fecha_ultima_entrada, categoria, observaciones, proveedor))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al insertar en inventario: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def Select_all(self):
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor()
            # La tabla en la BD se llama 'inventario' y los campos deben coincidir
            sql = """SELECT id_inventario, producto, cantidad_actual, precio_unitario, 
                            fecha_ultima_entrada, observaciones, categoria, proveedor 
                     FROM inventario"""
            cursor.execute(sql)
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            print(f"Error al seleccionar todo el inventario: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if con: con.close()
            
    def Update(
        self,
        id_inventario,
        producto,
        cantidad,
        precio,
        fecha,
        id_categoria,
        observaciones,
        id_proveedor
    ):
        con = self.get_conexion()
        cursor = con.cursor()

        try:
            sql = """
                UPDATE inventario
                SET producto = %s,
                    cantidad_actual = %s,
                    precio_unitario = %s,
                    fecha_ultima_entrada = %s,
                    categoria = %s,
                    observaciones = %s,
                    proveedor = %s
                WHERE id_inventario = %s
            """
            cursor.execute(sql, (
                producto,
                cantidad,
                precio,
                fecha,
                id_categoria,
                observaciones,
                id_proveedor,
                id_inventario
            ))
            con.commit()
            return cursor.rowcount

        finally:
            cursor.close()
            con.close()


    def Delete(self, id_inventario):
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor()
            sql = "DELETE FROM inventario WHERE id_inventario = %s"
            cursor.execute(sql, (id_inventario,))
            con.commit()
            return cursor.rowcount > 0 # Retorna True si se eliminó al menos 1 fila
        except Exception as e:
            print(f"Error al eliminar de inventario: {e}")
            # Si hay una restricción de clave foránea (ej: el producto está en una venta), fallará.
            return False
        finally:
            if cursor: cursor.close()
            if con: con.close()
            
    def buscar_por_nombre(self, producto, id_a_excluir=None):
        """
        Busca un producto por su nombre, opcionalmente excluyendo un ID.
        Hace la búsqueda sin distinguir mayúsculas/minúsculas.
        Retorna el primer resultado encontrado o None si no hay coincidencias.
        """
        con = None
        cursor = None
        try:
            con = self.get_conexion()
            cursor = con.cursor()
            
            query_sql = "SELECT id_inventario FROM inventario WHERE LOWER(producto) = LOWER(%s)"
            params = [producto]

            if id_a_excluir is not None:
                query_sql += " AND id_inventario != %s"
                params.append(id_a_excluir)
            
            cursor.execute(query_sql, tuple(params))
            resultado = cursor.fetchone()
            return resultado

        except Exception as e:
            print(f"Error al buscar producto por nombre: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def existe_producto(self, producto, id_excluir=None):
        con = self.get_conexion()
        cursor = con.cursor()
    
        try:
            if id_excluir:
                sql = """
                    SELECT 1 FROM inventario
                    WHERE LOWER(producto) = LOWER(%s)
                    AND id_inventario <> %s
                    LIMIT 1
                """
                cursor.execute(sql, (producto, id_excluir))
            else:
                sql = """
                    SELECT 1 FROM inventario
                    WHERE LOWER(producto) = LOWER(%s)
                    LIMIT 1
                """
                cursor.execute(sql, (producto,))

            return cursor.fetchone() is not None

        finally:
            cursor.close()
            con.close()

    # --- Métodos de gestión de transacciones (ya estaban bien) ---
    def iniciar_transaccion(self):
        try:
            self.con = self.get_conexion()
            self.con.start_transaction()
            print("[TRANSACCIÓN INVENTARIO] Iniciada.")
        except Exception as e:
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

    def obtener_stock_actual(self, id_inventario):
        if not self.con or not self.con.is_connected():
            print("Error: No hay conexión de transacción activa para obtener stock.")
            return None
        cursor = None
        try:
            sql = "SELECT cantidad_actual FROM inventario WHERE id_inventario = %s FOR UPDATE"
            cursor = self.con.cursor()
            cursor.execute(sql, (id_inventario,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener stock actual: {e}")
            return None
        finally:
            if cursor: cursor.close()

    def actualizar_stock(self, id_inventario, cambio_cantidad):
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
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()