# archivo: vistas/CompraView.py
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_compra import Controlador_compra

class CompraView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Compras")
        self.geometry("800x500")
        self.controlador = Controlador_compra()

        self._construir_interfaz()
        self._cargar_compras()

    def _construir_interfaz(self):
        self.lista = tk.Listbox(self, width=120)
        self.lista.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.e_id = tk.Entry(frame)
        self.e_id_cliente = tk.Entry(frame)
        self.e_fecha = tk.Entry(frame)
        self.e_total = tk.Entry(frame)

        etiquetas = ["ID Compra", "ID Cliente", "Fecha (YYYY-MM-DD)", "Total"]
        entradas = [self.e_id, self.e_id_cliente, self.e_fecha, self.e_total]

        for i, label in enumerate(etiquetas):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
            entradas[i].grid(row=i, column=1)

        tk.Button(self, text="Registrar Compra", command=self._registrar_compra).pack(pady=10)

    def _cargar_compras(self):
        self.lista.delete(0, tk.END)
        try:
            compras = self.controlador.obtener_todas_las_compras()
            if compras:
                for c in compras:
                    self.lista.insert(tk.END, f"ID: {c[0]} | Cliente: {c[1]} | Fecha: {c[2]} | Total: {c[3]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las compras: {e}")

    def _registrar_compra(self):
        id_compra = self.e_id.get()
        id_cliente = self.e_id_cliente.get()
        fecha = self.e_fecha.get()
        total = self.e_total.get()

        if id_compra and id_cliente and fecha and total:
            resultado = self.controlador.insertar_compra(id_compra, id_cliente, fecha, total)
            if resultado == 1:
                messagebox.showinfo("Éxito", "Compra registrada exitosamente")
                self._cargar_compras()
            else:
                messagebox.showerror("Error", f"No se pudo registrar la compra. Detalles: {resultado}")
        else:
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal si solo quieres mostrar el Toplevel
    ventana = CompraView(root)
    ventana.mainloop()