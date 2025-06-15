import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_categoria import Controlador_categoria

class CategoriaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Categorías")
        self.geometry("500x400")
        self.controlador = Controlador_categoria()

        self._construir_interfaz()
        self._cargar_categorias()

    def _construir_interfaz(self):
        self.lista = tk.Listbox(self, width=60)
        self.lista.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.e_id = tk.Entry(frame)
        self.e_nombre = tk.Entry(frame)

        etiquetas = ["ID Categoría", "Nombre"]
        entradas = [self.e_id, self.e_nombre]

        for i, label in enumerate(etiquetas):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
            entradas[i].grid(row=i, column=1)

        tk.Button(self, text="Agregar Categoría", command=self._agregar_categoria).pack(pady=10)

    def _cargar_categorias(self):
        self.lista.delete(0, tk.END)
        try:
            categorias = self.controlador.obtener_todas_las_categorias()
            if categorias:
                for c in categorias:
                    self.lista.insert(tk.END, f"ID: {c[0]} | Nombre: {c[1]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las categorías: {e}")

    def _agregar_categoria(self):
        id_cat = self.e_id.get()
        nombre = self.e_nombre.get()

        if id_cat and nombre:
            resultado = self.controlador.insertar_categoria(id_cat, nombre)
            if resultado == 1:
                messagebox.showinfo("Éxito", "Categoría agregada exitosamente")
                self._cargar_categorias()
            else:
                messagebox.showerror("Error", f"No se pudo agregar la categoría. Detalles: {resultado}")
        else:
            messagebox.showwarning("Campos requeridos", "ID y Nombre son obligatorios")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = CategoriaView(root)
    ventana.mainloop()