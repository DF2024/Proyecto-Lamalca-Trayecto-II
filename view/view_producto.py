# archivo: vistas/ProductoView.py
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_producto import Controlador_producto

class ProductoView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Productos")
        self.geometry("750x550")
        self.controlador = Controlador_producto()

        self._construir_interfaz()
        self._cargar_productos()

    def _construir_interfaz(self):
        self.lista = tk.Listbox(self, width=110)
        self.lista.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.e_id = tk.Entry(frame)
        self.e_nombre = tk.Entry(frame)
        self.e_precio = tk.Entry(frame)
        self.e_stock = tk.Entry(frame)
        self.e_id_seccion = tk.Entry(frame)

        etiquetas = ["ID", "Nombre", "Precio", "Stock", "ID Sección"]
        entradas = [self.e_id, self.e_nombre, self.e_precio, self.e_stock, self.e_id_seccion]

        for i, label in enumerate(etiquetas):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
            entradas[i].grid(row=i, column=1)

        tk.Button(self, text="Agregar Producto", command=self._agregar_producto).pack(pady=10)

    def _cargar_productos(self):
        self.lista.delete(0, tk.END)
        try:
            productos = self.controlador.obtener_todos_los_productos()
            if productos:
                for p in productos:
                    self.lista.insert(tk.END, f"ID: {p[0]} | Nombre: {p[1]} | Precio: {p[2]} | Stock: {p[3]} | Sección ID: {p[4]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los productos: {e}")

    def _agregar_producto(self):
        id_p = self.e_id.get()
        nombre = self.e_nombre.get()
        precio = self.e_precio.get()
        stock = self.e_stock.get()
        id_seccion = self.e_id_seccion.get()

        if id_p and nombre and precio and stock and id_seccion:
            resultado = self.controlador.insertar_producto(id_p, nombre, precio, stock, id_seccion)
            if resultado == 1:
                messagebox.showinfo("Éxito", "Producto agregado exitosamente")
                self._cargar_productos()
            else:
                messagebox.showerror("Error", f"No se pudo agregar el producto. Detalles: {resultado}")
        else:
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ProductoView(root)
    ventana.mainloop()