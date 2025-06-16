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
        self.e_descripcion = tk.Entry(frame)
        self.e_precio = tk.Entry(frame)
        self.e_stock = tk.Entry(frame)
        self.e_id_categoria = tk.Entry(frame)
        self.e_id_proveedor = tk.Entry(frame)

        etiquetas = ["ID", "Nombre", "Descripción" ,"Precio", "Stock", "ID Categoria", "Proovedor"]
        entradas = [self.e_id, self.e_nombre, self.e_descripcion, self.e_precio, self.e_stock, self.e_id_categoria, self.e_id_proveedor]

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
                    self.lista.insert(tk.END, f"ID: {p[0]} | Nombre: {p[1]} | Descripción: {p[2]} | Precio: {p[3]} | Stock: {p[4]} | Categoria ID: {p[5]} | Proveedor: {p[5]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los productos: {e}")

    def _agregar_producto(self):
        id_p = self.e_id.get()
        nombre = self.e_nombre.get()
        descripcion = self.e_descripcion.get()
        precio_venta = self.e_precio.get()
        stock = self.e_stock.get()
        id_categoria = self.e_id_categoria.get()
        id_proveedor = self.e_id_proveedor.get()

        if id_p and nombre and precio_venta and stock and id_categoria and id_proveedor:
            resultado = self.controlador.insertar_producto(id_p, nombre, descripcion, precio_venta, stock, id_categoria, id_proveedor)
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