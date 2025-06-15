# archivo: vistas/EntradaInventarioView.py
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_entrada_inventario import Controlador_entrada_inventario

class EntradaInventarioView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Entradas al Inventario")
        self.geometry("850x500")
        self.controlador = Controlador_entrada_inventario()

        self._construir_interfaz()
        self._cargar_entradas()

    def _construir_interfaz(self):
        self.lista = tk.Listbox(self, width=120)
        self.lista.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.e_id_entrada = tk.Entry(frame)
        self.e_id_producto = tk.Entry(frame)
        self.e_cantidad = tk.Entry(frame)
        self.e_fecha = tk.Entry(frame)

        etiquetas = ["ID Entrada", "ID Producto", "Cantidad", "Fecha (YYYY-MM-DD)"]
        entradas = [self.e_id_entrada, self.e_id_producto, self.e_cantidad, self.e_fecha]

        for i, label in enumerate(etiquetas):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
            entradas[i].grid(row=i, column=1)

        tk.Button(self, text="Registrar Entrada", command=self._registrar_entrada).pack(pady=10)

    def _cargar_entradas(self):
        self.lista.delete(0, tk.END)
        try:
            entradas = self.controlador.obtener_todas_las_entradas()
            if entradas:
                for e in entradas:
                    self.lista.insert(tk.END, f"ID: {e[0]} | Producto: {e[1]} | Cantidad: {e[2]} | Fecha: {e[3]}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar entradas: {ex}")

    def _registrar_entrada(self):
        id_entrada = self.e_id_entrada.get()
        id_producto = self.e_id_producto.get()
        cantidad = self.e_cantidad.get()
        fecha = self.e_fecha.get()

        if id_entrada and id_producto and cantidad and fecha:
            resultado = self.controlador.insertar_entrada(id_entrada, id_producto, cantidad, fecha)
            if resultado == 1:
                messagebox.showinfo("Éxito", "Entrada registrada exitosamente")
                self._cargar_entradas()
            else:
                messagebox.showerror("Error", f"No se pudo registrar la entrada. Detalles: {resultado}")
        else:
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal si solo quieres mostrar el Toplevel
    ventana = EntradaInventarioView(root)
    ventana.mainloop()