import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# archivo: vistas/ProveedorView.py
import tkinter as tk
from tkinter import messagebox
from controller.controller_proveedor import Controlador_proveedor

class ProveedorView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Proveedores")
        self.geometry("700x500")
        self.controlador = Controlador_proveedor()

        self._construir_interfaz()
        self._cargar_proveedores()

    def _construir_interfaz(self):
        self.lista = tk.Listbox(self, width=100)
        self.lista.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.e_id = tk.Entry(frame)
        self.e_nombre = tk.Entry(frame)
        self.e_tel = tk.Entry(frame)
        self.e_dir = tk.Entry(frame)

        for i, label in enumerate(["ID", "Nombre", "Teléfono", "Dirección"]):
            tk.Label(frame, text=label).grid(row=i, column=0)
        for i, entry in enumerate([self.e_id, self.e_nombre, self.e_tel, self.e_dir]):
            entry.grid(row=i, column=1)

        tk.Button(self, text="Agregar Proveedor", command=self._agregar_proveedor).pack(pady=10)

    def _cargar_proveedores(self):
        self.lista.delete(0, tk.END)
        proveedores = self.controlador.obtener_todos_los_proveedores()
        for p in proveedores:
            self.lista.insert(tk.END, f"ID: {p[0]} | Nombre: {p[1]} | Tel: {p[2]} | Dirección: {p[3]}")

    def _agregar_proveedor(self):
        id_p = self.e_id.get()
        nombre = self.e_nombre.get()
        tel = self.e_tel.get()
        dir_ = self.e_dir.get()

        if id_p and nombre:
            resultado = self.controlador.insertar_proveedor(id_p, nombre, tel, dir_)
            if resultado == 1:
                messagebox.showinfo("Éxito", "Proveedor agregado exitosamente")
                self._cargar_proveedores()
            else:
                messagebox.showerror("Error", "No se pudo agregar el proveedor")
        else:
            messagebox.showwarning("Campos requeridos", "ID y Nombre son obligatorios")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal si solo quieres mostrar el Toplevel
    ventana = ProveedorView(root)
    ventana.mainloop()