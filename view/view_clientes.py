# archivo: vistas/ClienteView.py
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_cliente import Controlador_cliente

class ClienteView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Clientes")
        self.geometry("700x500")
        self.controlador = Controlador_cliente()

        self._construir_interfaz()
        self._cargar_clientes()

    def _construir_interfaz(self):
        self.lista = tk.Listbox(self, width=100)
        self.lista.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.e_nombre = tk.Entry(frame)
        self.e_apellido = tk.Entry(frame)
        self.e_cedula = tk.Entry(frame)
        self.e_telefono = tk.Entry(frame)
        self.e_direccion = tk.Entry(frame)

        etiquetas = ["Nombre", "Apellido", "Cédula", "Teléfono", "Dirección"]
        entradas = [self.e_nombre, self.e_apellido, self.e_cedula, self.e_telefono, self.e_direccion]

        for i, label in enumerate(etiquetas):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
            entradas[i].grid(row=i, column=1)

        tk.Button(self, text="Agregar Cliente", command=self._agregar_cliente).pack(pady=10)

    def _cargar_clientes(self):
        self.lista.delete(0, tk.END)
        try:
            clientes = self.controlador.obtener_todos_los_clientes()
            if clientes:
                for c in clientes:
                    self.lista.insert(tk.END, f"Nombre: {c[1]} {c[2]} | Cédula: {c[3]} | Tel: {c[4]} | Dirección: {c[5]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los clientes: {e}")

    def _agregar_cliente(self):
        nombre = self.e_nombre.get()
        apellido = self.e_apellido.get()
        cedula = self.e_cedula.get()
        telefono = self.e_telefono.get()
        direccion = self.e_direccion.get()

        if nombre and apellido:
            resultado = self.controlador.insertar_cliente(nombre, apellido, cedula, telefono, direccion)
            if resultado == 1:
                messagebox.showinfo("Éxito", "Cliente agregado exitosamente")
                self._cargar_clientes()
            else:
                messagebox.showerror("Error", f"No se pudo agregar el cliente. Detalles: {resultado}")
        else:
            messagebox.showwarning("Campos requeridos", "ID, Nombre y Apellido son obligatorios")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ClienteView(root)
    ventana.mainloop()