# archivo: vistas/DetalleEntradaView.py
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_detalle_entrada import Controlador_detalle_entrada

class DetalleEntradaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Detalles de Entrada")
        self.geometry("900x500")
        self.controlador = Controlador_detalle_entrada()

        self._construir_interfaz()
        self._cargar_detalles()

    def _construir_interfaz(self):
        self.lista = tk.Listbox(self, width=130)
        self.lista.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.e_id_detalle = tk.Entry(frame)
        self.e_id_entrada = tk.Entry(frame)
        self.e_id_producto = tk.Entry(frame)
        self.e_cantidad = tk.Entry(frame)
        self.e_precio_unitario = tk.Entry(frame)

        etiquetas = ["ID Detalle", "ID Entrada", "ID Producto", "Cantidad", "Precio Unitario"]
        entradas = [self.e_id_detalle, self.e_id_entrada, self.e_id_producto, self.e_cantidad, self.e_precio_unitario]

        for i, label in enumerate(etiquetas):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
            entradas[i].grid(row=i, column=1)

        tk.Button(self, text="Agregar Detalle Entrada", command=self._agregar_detalle).pack(pady=10)

    def _cargar_detalles(self):
        self.lista.delete(0, tk.END)
        try:
            detalles = self.controlador.obtener_todos_los_detalles()
            if detalles:
                for d in detalles:
                    self.lista.insert(tk.END, f"ID: {d[0]} | Entrada: {d[1]} | Producto: {d[2]} | Cantidad: {d[3]} | Precio: {d[4]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los detalles: {e}")

    def _agregar_detalle(self):
        id_det = self.e_id_detalle.get()
        id_entrada = self.e_id_entrada.get()
        id_producto = self.e_id_producto.get()
        cantidad = self.e_cantidad.get()
        precio = self.e_precio_unitario.get()

        if id_det and id_entrada and id_producto and cantidad and precio:
            resultado = self.controlador.insertar_detalle(id_det, id_entrada, id_producto, cantidad, precio)
            if resultado == 1:
                messagebox.showinfo("Éxito", "Detalle de entrada agregado exitosamente")
                self._cargar_detalles()
            else:
                messagebox.showerror("Error", f"No se pudo agregar el detalle. Detalles: {resultado}")
        else:
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal si solo quieres mostrar el Toplevel
    ventana = DetalleEntradaView(root)
    ventana.mainloop()