import tkinter as tk
from tkinter import messagebox
from view.view_clientes import ClienteView
from view.view_compra import CompraView
from view.view_producto import ProductoView

# Simulaciones de vistas (reemplaza por tus clases reales)

class EmpleadoDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Empleado")
        self.geometry("350x350")
        tk.Label(self, text="Panel de Empleado", font=("Arial", 16)).pack(pady=20)

        botones = [
            ("Clientes", self.abrir_cliente),
            ("Compras", self.abrir_compra),
            ("Productos", self.abrir_producto),
        ]

        for texto, comando in botones:
            tk.Button(self, text=texto, width=25, command=comando).pack(pady=10)

    def abrir_cliente(self):
        ClienteView(self)

    def abrir_compra(self):
        CompraView(self)

    def abrir_producto(self):
        ProductoView(self)

if __name__ == "__main__":
    app = EmpleadoDashboard()
    app.mainloop()