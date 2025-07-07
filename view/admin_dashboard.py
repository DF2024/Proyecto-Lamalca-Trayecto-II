# view/admin_dashboard.py
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import sys

# --- Dependencia para iconos ---
try:
    from PIL import Image
    iconos_disponibles = True
except ImportError:
    iconos_disponibles = False
# ------------------------------

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Importamos todas las vistas que el admin puede abrir
from view.view_proveedor import ProveedorView
from view.view_inventario import InventarioView
from view.view_categoria import CategoriaView
from view.view_compra import CompraView
from view.view_cierre_caja import CierreCajaView

class AdminDashboard(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Panel de Administración - Sistema La Malca")
        self.geometry("900x600")
        self.resizable(False, False)
        
        # Centrar la ventana al iniciar
        self.after(200, lambda: self.eval('tk::PlaceWindow . center'))

        # --- Tema Oscuro ---
        # No es necesario setearlo aquí si ya se hizo en el login, pero no hace daño
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.iconos = {}
        if iconos_disponibles:
            self._cargar_iconos()
        
        self._construir_interfaz()

    def _cargar_iconos(self):
        icon_path = "icons"
        if not os.path.isdir(icon_path): return

        icon_files = {
            "inventario": "inventory_icon_light.png",
            "proveedores": "suppliers_icon_light.png",
            "categorias": "category_icon_light.png",
            "ventas": "sales_icon_light.png",
            "caja": "cashier_icon_light.png",
            "logout": "logout_icon_light.png"
        }
        for name, filename in icon_files.items():
            try:
                path = os.path.join(icon_path, filename)
                image_pil = Image.open(path)
                self.iconos[name] = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=(48, 48))
            except Exception as e:
                print(f"Advertencia: No se pudo cargar el icono '{filename}': {e}")
    
    def _construir_interfaz(self):
        # --- Frame principal con padding ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # --- Cabecera ---
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 30))
        
        ctk.CTkLabel(header_frame, text="Panel de Administración", font=ctk.CTkFont(size=32, weight="bold")).pack()
        ctk.CTkLabel(header_frame, text="Seleccione una opción para comenzar a gestionar", font=ctk.CTkFont(size=14), text_color="#a0a0a0").pack()

        # --- Cuadrícula de Botones (Tarjetas de Módulos) ---
        grid_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        
        # Configurar la cuadrícula para que se centre y expanda
        grid_frame.grid_columnconfigure((0, 1, 2), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)
        
        # --- Opciones del Dashboard ---
        opciones = [
            {"texto": "Gestionar Inventario", "icono": self.iconos.get("inventario"), "comando": lambda: self._abrir_ventana(InventarioView)},
            {"texto": "Gestionar Proveedores", "icono": self.iconos.get("proveedores"), "comando": lambda: self._abrir_ventana(ProveedorView)},
            {"texto": "Gestionar Categorías", "icono": self.iconos.get("categorias"), "comando": lambda: self._abrir_ventana(CategoriaView)},
        ]
        
        # Crear los botones en la cuadrícula
        for i, opcion in enumerate(opciones):
            fila = i // 3
            columna = i % 3
            
            # Tarjeta/Frame para cada botón
            card = ctk.CTkFrame(grid_frame, corner_radius=15, fg_color="#2b2b2b")
            card.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
            
            # Botón dentro de la tarjeta
            btn = ctk.CTkButton(card, text=opcion["texto"], image=opcion["icono"], 
                                font=ctk.CTkFont(size=14, weight="bold"),
                                compound="top", fg_color="transparent",
                                hover_color="#3b3b3b", command=opcion["comando"],
                                text_color_disabled="#777777")
            btn.pack(expand=True, fill="both", padx=10, pady=10)
        
        # --- Botón de Cerrar Sesión ---
        logout_button = ctk.CTkButton(main_frame, text="Cerrar Sesión", image=self.iconos.get("logout"),
                                      compound="left", command=self.cerrar_sesion,
                                      fg_color="#c0392b", hover_color="#e74c3c", # Tonos de rojo
                                      font=ctk.CTkFont(size=12, weight="bold"), height=35)
        logout_button.pack(side="bottom", anchor="se", pady=(20, 0), padx=(0, 10))

    def _abrir_ventana(self, VentanaClase):
        self.withdraw() # Ocultamos el dashboard
        ventana_gestion = VentanaClase(master=self)
        # Cuando se cierre la ventana de gestión, mostramos el dashboard de nuevo
        ventana_gestion.protocol("WM_DELETE_WINDOW", lambda: self._al_cerrar_ventana_gestion(ventana_gestion))
    
    def _al_cerrar_ventana_gestion(self, ventana):
        ventana.destroy()
        self.deiconify() # Vuelve a mostrar el dashboard

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar la sesión?"):
            self.destroy()
            self.master.deiconify() # Muestra la ventana de login