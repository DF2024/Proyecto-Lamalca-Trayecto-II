# login.py
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
import view.admin_dashboard as admin
import view.empleado_dashboard as emple

# <<-- Cambio Fundamental: Hereda de ctk.CTk en lugar de tk.Tk -->>
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesión - Sistema La Malca")
        self.geometry("800x550")
        self.resizable(False, False)
        
        # Centrar la ventana al iniciar
        self.after(200, lambda: self.eval('tk::PlaceWindow . center'))

        # --- Tema Oscuro ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.iconos = {}
        if iconos_disponibles:
            self._cargar_iconos()
        
        self._construir_interfaz()

    def _cargar_iconos(self):
        # Asegúrate de que la carpeta 'icons' está en la misma raíz que tu script principal
        icon_path = "icons" 
        if not os.path.isdir(icon_path):
            print(f"Advertencia: No se encontró la carpeta de iconos en: {os.path.abspath(icon_path)}")
            return

        icon_files = {
            "logo": "logo.png", "user": "user_icon_light.png", "lock": "lock_icon_light.png",
            "show": "show_password_light.png", "hide": "hide_password_light.png"
        }
        for name, filename in icon_files.items():
            try:
                path = os.path.join(icon_path, filename)
                image_pil = Image.open(path)
                size = (180, 180) if name == "logo" else (20, 20)
                self.iconos[name] = ctk.CTkImage(light_image=image_pil, dark_image=image_pil, size=size)
            except FileNotFoundError:
                print(f"Advertencia: No se encontró el icono '{filename}'")
            except Exception as e:
                print(f"Error al cargar icono '{filename}': {e}")

    def _construir_interfaz(self):
        # --- Diseño de dos paneles ---
        self.grid_columnconfigure(0, weight=2) # Panel izquierdo más pequeño
        self.grid_columnconfigure(1, weight=3) # Panel derecho más grande
        self.grid_rowconfigure(0, weight=1)

        # --- Panel Izquierdo (Branding/Logo) ---
        left_panel = ctk.CTkFrame(self, fg_color="#242424", corner_radius=0)
        left_panel.grid(row=0, column=0, sticky="nsew")
        
        logo_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        logo_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        logo_label = ctk.CTkLabel(logo_frame, text="", image=self.iconos.get("logo"))
        logo_label.pack(pady=(0, 20))
        
        ctk.CTkLabel(logo_frame, text="Ferretería La Malca", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 5))
        ctk.CTkLabel(logo_frame, text="Sistema de Gestión", font=ctk.CTkFont(size=14), text_color="#a0a0a0").pack()
        
        # --- Panel Derecho (Formulario de Login) ---
        right_panel = ctk.CTkFrame(self, fg_color="#2e2e2e", corner_radius=0)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        login_form_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        login_form_frame.place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(login_form_frame, text="Iniciar Sesión", font=ctk.CTkFont(size=32, weight="bold")).pack(pady=(0, 40))

        # --- Campo de Usuario con Icono ---
        self.user_entry = ctk.CTkEntry(login_form_frame, placeholder_text="Usuario", 
                                       font=ctk.CTkFont(size=14), width=300, height=45,
                                       border_width=1, corner_radius=10)
        self.user_entry.pack(pady=10)

        # --- Campo de Contraseña con Icono y Botón de Visibilidad ---
        self.pass_entry = ctk.CTkEntry(login_form_frame, show="*", placeholder_text="Contraseña", 
                                       font=ctk.CTkFont(size=14), width=300, height=45,
                                       border_width=1, corner_radius=10)
        self.pass_entry.pack(pady=10)
        
        self.show_pass_button = ctk.CTkButton(self.pass_entry, text="", image=self.iconos.get("show"), 
                                              width=30, height=30, fg_color="transparent", 
                                              hover_color="#444444", command=self.toggle_password_visibility)
        self.show_pass_button.place(relx=0.9, rely=0.5, anchor="center")

        self.pass_entry.bind("<Return>", self.login)
        self.user_entry.focus()
        
        # --- Botón de Iniciar Sesión ---
        login_button = ctk.CTkButton(login_form_frame, text="Acceder", 
                                     font=ctk.CTkFont(size=16, weight="bold"), 
                                     height=45, width=300, corner_radius=10,
                                     command=self.login)
        login_button.pack(pady=(40, 15))

    def toggle_password_visibility(self):
        if self.pass_entry.cget("show") == "*":
            self.pass_entry.configure(show="")
            self.show_pass_button.configure(image=self.iconos.get("hide"))
        else:
            self.pass_entry.configure(show="*")
            self.show_pass_button.configure(image=self.iconos.get("show"))

    def login(self, event=None):
        usuario = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese su usuario y contraseña.")
            return

        usuarios = {
            "admin": {"password": "123", "rol": "admin"},
            "empleado": {"password": "456", "rol": "empleado"}
        }

        if usuario in usuarios and usuarios[usuario]["password"] == password:
            rol = usuarios[usuario]["rol"]
            self.withdraw()
            
            dashboard = None
            if rol == "admin":
                dashboard = admin.AdminDashboard(master=self)
            elif rol == "empleado":
                dashboard = emple.EmpleadoDashboard(master=self)
            
            if dashboard:
                dashboard.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
            else:
                messagebox.showerror("Error de Configuración", f"El rol '{rol}' no tiene un dashboard asignado.")
                self.deiconify()
        else:
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")
            self.pass_entry.delete(0, 'end')
            self.pass_entry.focus()

    def on_dashboard_close(self):
        self.destroy()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()