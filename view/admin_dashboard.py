# dashboard_admin.py
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from view.view_proveedor import ProveedorView
from view.view_producto import ProductoView
from view.view_categoria import CategoriaView

class AdminDashboard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Dashboard - Administrador")
        self.geometry("700x500")

        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("green")  


        self.master.eval(f'tk::PlaceWindow {self.winfo_pathname(self.winfo_id())} center')

        style = ttk.Style(self)
        style.configure("Dashboard.TButton", font=("Arial", 12), padding=10)

        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(expand=True, fill="both")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(main_frame, text="Panel de Administración", font=("Arial", 24, "bold")).pack(pady=(0, 20))

        # Opciones para el Administrador
        botones = [
            ("Gestionar Proveedores", ProveedorView),
            ("Gestionar Productos", ProductoView),
            ("Gestionar Categorías", CategoriaView)
        ]

        for texto, VentanaClase in botones:
            ttk.Button(main_frame, text=texto,
                    command=lambda vc=VentanaClase: self._abrir_ventana(vc),
                    style="Dashboard.TButton", width=50).pack(fill="x", pady=5)

        logout_button = ctk.CTkButton(main_frame, text="Cerrar Sesión", font=("Arial", 15, "bold"), command=self.cerrar_sesion)
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