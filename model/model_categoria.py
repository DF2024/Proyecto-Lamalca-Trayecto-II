import os
import sys
# Asegura que se pueda encontrar la clase de conexión en el directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.conexion import Conexion
from mysql.connector import Error

class Modelo_categoria(Conexion):
    def __init__(self):
        super().__init__()
        # self.con ahora almacena el objeto de conexión
        self.con = self.get_conexion()
        # self.cursor se puede inicializar aquí para reutilizarlo o dentro de cada método
        self.cursor = self.con.cursor()

    def Insert(self, nombre):
        """
        Inserta una nueva categoría.
        Retorna el número de filas afectadas (1 si fue exitoso, 0 si no).
        """
        try:
            # CORRECCIÓN: La consulta SQL solo debe tener un marcador de posición %s para el campo 'nombre'.
            sql = '''
                INSERT INTO categorias (nombre)
                VALUES (%s) 
            '''
            # El valor se pasa como una tupla, incluso si es solo un elemento.
            self.cursor.execute(sql, (nombre,))
            self.con.commit()
            # Retornamos el número de filas insertadas.
            return self.cursor.rowcount
        except Error as e:
            print(f"Error al insertar categoría: {e}")
            # En caso de error, retornamos 0 para indicar que no se insertó nada.
            return 0

    def Select_all(self):
        """
        Selecciona todas las categorías.
        Retorna una lista de tuplas con los datos.
        """
        try:
            self.cursor.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
            # CORRECIÓN: Es importante usar el nombre de columna real de tu tabla (ej. id_categoria)
            info = self.cursor.fetchall()
            return info
        except Error as e:
            print(f"Error al seleccionar todas las categorías: {e}")
            return [] # Retornar una lista vacía en caso de error es una buena práctica.

    def Update(self, id_categoria, nombre):
        """
        Actualiza una categoría existente.
        Retorna el número de filas afectadas.
        """
        try:
            sql = '''
                UPDATE categorias
                SET nombre = %s
                WHERE id_categoria = %s
            '''
            self.cursor.execute(sql, (nombre, id_categoria))
            self.con.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Error al actualizar categoría: {e}")
            return 0

    def Delete(self, id_categoria):
        """
        Elimina una categoría por su ID.
        Retorna el número de filas afectadas.
        """
        try:
            sql = "DELETE FROM categorias WHERE id_categoria = %s"
            self.cursor.execute(sql, (id_categoria,))
            self.con.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Error al eliminar categoría: {e}")
            # Este error puede ocurrir si la categoría es una clave foránea en otra tabla.
            return 0


