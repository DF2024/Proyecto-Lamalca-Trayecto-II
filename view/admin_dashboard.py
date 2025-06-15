import tkinter as tk
from tkinter import messagebox
from view.view_proveedor import ProveedorView
from view.view_producto import ProductoView
from view.view_entrada_inventario import EntradaInventarioView
from view.view_detalle_entrada import DetalleEntradaView
from view.view_categoria import CategoriaView


class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Administrador")
        self.geometry("400x400")
        tk.Label(self, text="Panel de Administración", font=("Arial", 16)).pack(pady=20)

        botones = [
            ("Proveedores", self.abrir_proveedor),
            ("Productos", self.abrir_producto),
            ("Entradas", self.abrir_entrada),
            ("Detalle Entrada", self.abrir_detalle_entrada),
            ("Categorías", self.abrir_categoria),
        ]

        for texto, comando in botones:
            tk.Button(self, text=texto, width=25, command=comando).pack(pady=8)

    def abrir_proveedor(self):
        ProveedorView(self)

    def abrir_producto(self):
        ProductoView(self)

    def abrir_entrada(self):
        EntradaInventarioView(self)

    def abrir_detalle_entrada(self):
        DetalleEntradaView(self)

    def abrir_categoria(self):
        CategoriaView(self)

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()