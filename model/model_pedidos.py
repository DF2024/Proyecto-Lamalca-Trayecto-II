# id_pedido 
# id_cliente 
# fecha_pedido 
# estado_pedido  
# total_pedido 

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error
from datetime import date


class Modelo_pedido(Conexion):
    def __init__(self):
        super().__init__()
        self.con = self.get_conexion()
        if not self.con:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

    def _execute_query(self, sql, params=None, fetch_one=False, fetch_all=False):
        """
        Método auxiliar para ejecutar consultas SQL, manejar errores comunes
        y gestionar el ciclo de vida del cursor.
        """
        if not self.con or not self.con.is_connected():
            print("Error: No hay conexión a la base de datos o la conexión está cerrada.")
            return None

        cursor = None
        try:
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            if sql.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                self.con.commit()
                return cursor.rowcount # Retorna el número de filas afectadas
            elif fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            return None
        except Error as e:
            self.con.rollback() # Deshace los cambios en caso de error para operaciones DML
            print(f"Error en la consulta SQL: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


    def Insert(self, id_cliente, fecha_pedido,  total):
        """
        Inserta un nuevo pedido en la tabla 'pedidos'.
        Args:
            id_cliente (int): ID del cliente asociado al pedido.
            fecha_pedido (datetime.date): Fecha del pedido.
            estado_pedido (str): Estado del pedido (ej. 'Pendiente', 'Enviado').
            total_pedido (float/Decimal): Monto total del pedido.
        Returns:
            int: Número de filas afectadas (1 si fue exitoso), o None en caso de error.
        """
        sql = """
            INSERT INTO pedidos (id_cliente, fecha_pedido, total)
            VALUES (%s, %s, %s)
        """
        # Asegúrate de que fecha_pedido sea un objeto date
        if not isinstance(fecha_pedido, date):
            print("Advertencia: fecha_pedido no es un objeto date. Usando la fecha actual.")
            fecha_pedido = date.today()

        return self._execute_query(sql, (id_cliente, fecha_pedido, total))

    def Select(self, id_pedido):
        """
        Selecciona un pedido por su ID, incluyendo el nombre y email del cliente asociado.
        Returns:
            tuple: Una tupla con (id_pedido, id_cliente, nombre_cliente, email_cliente, fecha_pedido, estado_pedido, total_pedido),
                o None si no se encuentra.
        """
        sql = """
            SELECT p.id_pedido, p.id_cliente, c.nombre AS cliente_nombre, c.email AS cliente_email,
                p.fecha_pedido, p.total_pedido
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.id_pedido = %s
        """
        return self._execute_query(sql, (id_pedido,), fetch_one=True)

    def Update(self, id_pedido, new_id_cliente=None, new_fecha_pedido=None, new_total_pedido=None):
        """
        Actualiza los campos de un pedido existente.
        Solo los campos no nulos se actualizarán.
        Returns:
            int: Número de filas afectadas.
        """
        updates = []
        params = []

        if new_id_cliente is not None:
            updates.append("id_cliente = %s")
            params.append(new_id_cliente)
        if new_fecha_pedido is not None:
            updates.append("fecha_pedido = %s")
            params.append(new_fecha_pedido)
        if new_total_pedido is not None:
            updates.append("total = %s")
            params.append(new_total_pedido)

        if not updates:
            print("No se proporcionaron campos para actualizar.")
            return 0

        sql = f"UPDATE pedidos SET {', '.join(updates)} WHERE id_pedido = %s"
        params.append(id_pedido) # El ID del pedido va al final de los parámetros

        return self._execute_query(sql, tuple(params))

    def Delete(self, id_pedido):
        """
        Elimina un pedido de la tabla 'pedidos' por su ID.
        Returns:
            int: Número de filas afectadas.
        """
        sql = "DELETE FROM pedidos WHERE id_pedido = %s"
        return self._execute_query(sql, (id_pedido,))

    def delete_pedidos_by_cliente(self, id_cliente):
        """
        Elimina todos los pedidos asociados a un cliente específico.
        Returns:
            int: Número de filas afectadas.
        """
        sql = "DELETE FROM pedidos WHERE id_cliente = %s"
        return self._execute_query(sql, (id_cliente,))

    def select_all(self):
        """
        Selecciona todos los pedidos, incluyendo el nombre y email de sus clientes.
        Returns:
            list of tuples: Lista de todos los pedidos con información del cliente.
        """
        sql = """
            SELECT p.id_pedido, p.id_cliente, c.nombre AS cliente_nombre, c.email AS cliente_email,
                p.fecha_pedido, p.total_pedido
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            ORDER BY p.fecha_pedido DESC
        """
        return self._execute_query(sql, fetch_all=True)


pedido1 = Modelo_pedido()
resultado = pedido1.Insert(1, date(2003,6,29), 3000)



















# --- EJEMPLO DE USO ---
# if __name__ == "__main__":
#     try:
#         # Crea una instancia del modelo de pedidos
#         modelo_pedidos = Modelo_pedido()

#         # Asegura que las tablas existan en tu base de datos MySQL
#         modelo_pedidos.create_tables_if_not_exists()

#         print("\n--- Insertando clientes de prueba ---")
#         id_cliente_carlos = modelo_pedidos.insert_cliente("Carlos Ruiz", "carlos.ruiz@ejemplo.com")
#         id_cliente_laura = modelo_pedidos.insert_cliente("Laura Gámez", "laura.g@ejemplo.com")

#         if id_cliente_carlos is not None and id_cliente_laura is not None:
#             print("\n--- Insertando pedidos de prueba ---")
#             # Usa la fecha actual si no se especifica
#             modelo_pedidos.insert_pedido(id_cliente_carlos, date.today(), "Pendiente", 550.25)
#             modelo_pedidos.insert_pedido(id_cliente_carlos, date(2025, 5, 10), "Enviado", 120.00)
#             modelo_pedidos.insert_pedido(id_cliente_laura, date.today(), "Procesando", 80.50)

#             print("\n--- Seleccionando todos los pedidos ---")
#             all_pedidos = modelo_pedidos.select_all_pedidos()
#             if all_pedidos:
#                 print("ID Pedido | ID Cliente | Nombre Cliente | Email Cliente      | Fecha      | Estado     | Total")
#                 print("----------|------------|----------------|--------------------|------------|------------|--------")
#                 for p in all_pedidos:
#                     print(f"{p[0]:<9} | {p[1]:<10} | {p[2]:<14} | {p[3]:<18} | {p[4]} | {p[5]:<10} | ${p[6]:<6.2f}")
#             else:
#                 print("No se encontraron pedidos.")

#             # Para seleccionar un pedido específico, necesitamos su ID
#             # Tomaremos el ID del primer pedido de la lista para el ejemplo
#             if all_pedidos:
#                 first_pedido_id = all_pedidos[0][0]
#                 print(f"\n--- Seleccionando un pedido específico (ID: {first_pedido_id}) ---")
#                 single_pedido = modelo_pedidos.select_pedido(first_pedido_id)
#                 if single_pedido:
#                     print(f"Pedido encontrado: ID={single_pedido[0]}, Cliente='{single_pedido[2]}', "
#                         f"Estado='{single_pedido[5]}', Total='${single_pedido[6]:.2f}'")
#                 else:
#                     print(f"Pedido con ID {first_pedido_id} no encontrado.")
#             else:
#                 print("No hay pedidos para seleccionar por ID.")

#             print("\n--- Actualizando un pedido (estado y total del primer pedido) ---")
#             if all_pedidos:
#                 update_result = modelo_pedidos.update_pedido(first_pedido_id,
#                                                             new_estado_pedido="Entregado",
#                                                             new_total_pedido=560.00)
#                 print(f"Filas actualizadas: {update_result}")

#                 print("\n--- Verificando pedido actualizado ---")
#                 updated_pedido = modelo_pedidos.select_pedido(first_pedido_id)
#                 if updated_pedido:
#                     print(f"Pedido actualizado: ID={updated_pedido[0]}, Estado='{updated_pedido[5]}', Total='${updated_pedido[6]:.2f}'")

#             print(f"\n--- Eliminando pedidos del cliente {id_cliente_laura} ---")
#             delete_by_client_result = modelo_pedidos.delete_pedidos_by_cliente(id_cliente_laura)
#             print(f"Pedidos eliminados para cliente {id_cliente_laura}: {delete_by_client_result}")

#             print("\n--- Pedidos restantes después de la eliminación ---")
#             remaining_pedidos = modelo_pedidos.select_all_pedidos()
#             if remaining_pedidos:
#                 print("ID Pedido | ID Cliente | Nombre Cliente | Estado")
#                 print("----------|------------|----------------|--------")
#                 for p in remaining_pedidos:
#                     print(f"{p[0]:<9} | {p[1]:<10} | {p[2]:<14} | {p[5]:<10}")
#             else:
#                 print("No quedan pedidos.")
#         else:
#             print("No se pudieron crear clientes de prueba. Asegúrate de que tu base de datos esté configurada.")

#     except Exception as e:
#         print(f"Ha ocurrido un error inesperado: {e}")
#     finally:
#         # Asegúrate de cerrar la conexión al finalizar
#         if 'modelo_pedidos' in locals():
#             modelo_pedidos.close_conexion()