# model/model_producto.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error

class Modelo_producto(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()

    def Insert(self, nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor):
        # CORRECCIÓN 1: Se eliminó id_producto de los parámetros.
        # La base de datos debe encargarse de generar el ID con AUTO_INCREMENT.
        # Pasar el ID manualmente puede causar errores de clave duplicada.
        cursor = None  # Definir fuera del try para que exista en el finally
        try:
            cursor = self.con.cursor()
            sql = '''
                INSERT INTO productos (nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            # CORRECCIÓN 2: Los valores ahora coinciden con los parámetros sin el id_producto.
            valores = (nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount # Retorna 1 si fue exitoso
        except Error as e:
            # MEJORA: Imprimir el error para depuración y retornar 0 para indicar fallo.
            print(f"Error al insertar producto: {e}")
            return 0
        finally:
            # MEJORA: Asegurarse de que el cursor siempre se cierre.
            if cursor:
                cursor.close()

    def Select_all(self):
        # NOTA: Este Select_all funciona perfectamente con la Vista que te di,
        # porque la Vista es la que se encarga de "traducir" los IDs a nombres.
        cursor = None
        try:
            cursor = self.con.cursor()
            # Devolvemos los IDs, la vista hará el resto.
            sql = "SELECT id_producto, nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor FROM productos ORDER BY nombre"
            cursor.execute(sql)
            info = cursor.fetchall()
            return info
        except Error as e:
            print(f"Error al seleccionar todos los productos: {e}")
            return [] # Retornar lista vacía en caso de error.
        finally:
            if cursor:
                cursor.close()
    
    def Update(self, id_producto, nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor):
        # CORRECCIÓN 3: Se usó 'precio_venta' para ser consistente con la tabla y el Insert.
        # Tu código original tenía 'precio' aquí, pero 'precio_venta' en el Insert.
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = '''
                UPDATE productos
                SET nombre = %s, descripcion = %s, precio_venta = %s, stock = %s, id_categoria = %s, id_proveedor = %s
                WHERE id_producto = %s
            '''
            valores = (nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor, id_producto)
            cursor.execute(sql, valores)
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al actualizar producto: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def Delete(self, id_producto):
        cursor = None
        try:
            cursor = self.con.cursor()
            sql = "DELETE FROM productos WHERE id_producto = %s"
            cursor.execute(sql, (id_producto,))
            self.con.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al eliminar producto: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    # El método Select(id_producto) de tu código original está bien,
    # puedes mantenerlo si lo necesitas para otras funcionalidades.

    def __del__(self):
        if self.con and self.con.is_connected():
            self.con.close()