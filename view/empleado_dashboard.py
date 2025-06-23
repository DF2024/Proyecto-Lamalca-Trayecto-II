# dashboard_empleado.py
import tkinter as tk
from tkinter import ttk, messagebox

# Importa las vistas específicas para el empleado
from view.view_clientes import ClienteView
from view.view_compra import CompraView
from view.view_producto import ProductoView

class EmpleadoDashboard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Dashboard - Empleado")
        self.geometry("600x400")

        # ----- ¡AQUÍ ESTÁ LA CORRECCIÓN! -----
        self.master.eval(f'tk::PlaceWindow {self.winfo_pathname(self.winfo_id())} center')

        style = ttk.Style(self)
        style.configure("Dashboard.TButton", font=("Arial", 12), padding=10)

        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="Panel de Empleado", font=("Arial", 24, "bold")).pack(pady=(0, 20))

        botones = [
            ("Gestionar Clientes", ClienteView),
            ("Registrar Compras", CompraView),
            ("Consultar Productos", ProductoView)
        ]

        for texto, VentanaClase in botones:
            ttk.Button(main_frame, text=texto,
                    command=lambda vc=VentanaClase: self._abrir_ventana(vc),
                    style="Dashboard.TButton").pack(fill="x", pady=5)

        logout_button = ttk.Button(main_frame, text="Cerrar Sesión", command=self.cerrar_sesion)
        logout_button.pack(side="bottom", pady=(20, 0))

    def _abrir_ventana(self, VentanaClase):
        self.withdraw()
        ventana_gestion = VentanaClase(master=self)
        ventana_gestion.protocol("WM_DELETE_WINDOW", lambda: self._al_cerrar_ventana_gestion(ventana_gestion))
    
    def _al_cerrar_ventana_gestion(self, ventana):
        ventana.destroy()
        self.deiconify()

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar la sesión?"):
            self.destroy()
            self.master.deiconify()