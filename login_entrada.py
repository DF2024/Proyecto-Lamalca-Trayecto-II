# login.py
import tkinter as tk
from tkinter import messagebox, ttk
import view.admin_dashboard as admin # Importamos el dashboard del admin
import view.empleado_dashboard as emple# Importamos el dashboard del empleado
import customtkinter as ctk #Libreria de CustomTK


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesión - Sistema La Malca")
        self.geometry("700x500")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center') 


        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("green")  


        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")


        Labeltitle = ctk.CTkLabel(main_frame, text="Bienvenido", font=("Arial", 40, "bold"))
        Labeltitle.grid(row=0, column=1, padx=5, pady=10)

        self.user_entry = ctk.CTkEntry(main_frame, placeholder_text="Usuario", font=("Arial", 18), width=300, height=30)
        self.user_entry.grid(row=1, column=1, padx=5, pady=10)

        self.pass_entry = ctk.CTkEntry(main_frame, show="*", placeholder_text="Contraseña", font=("Arial", 18), width=300, height=30)
        self.pass_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.pass_entry.bind("<Return>", self.login)
        self.user_entry.focus() # Pone el cursor en el campo de usuario al iniciar

        login_button = ctk.CTkButton(main_frame, text="Iniciar Sesión", font=("Arial", 15, "bold"), command=self.login)
        login_button.grid(row=3, column=1, columnspan=2, pady=15)



    def login(self, event=None):
        usuario = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        # Base de datos de usuarios (simulada)
        usuarios = {
            "admin": {"password": "123", "rol": "admin"},
            "empleado": {"password": "456", "rol": "empleado"}
        }

        # 1. Validar si el usuario existe y la contraseña es correcta
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            rol = usuarios[usuario]["rol"]
            
            # 2. Ocultar la ventana de login
            self.withdraw()
            
            # 3. Decidir qué dashboard abrir basado en el rol
            if rol == "admin":
                # Se crea Y se maneja el cierre en el mismo bloque
                dashboard = admin.AdminDashboard(master=self)
                dashboard.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
            elif rol == "empleado":
                # Se crea Y se maneja el cierre en el mismo bloque
                dashboard = emple.EmpleadoDashboard(master=self)
                dashboard.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
            else:
                # Este 'else' ahora SÍ tiene sentido: el rol existe en el diccionario pero no hay un dashboard para él.
                messagebox.showerror("Error de Configuración", f"El rol '{rol}' es válido pero no tiene un dashboard asignado.")
                self.deiconify() # Vuelve a mostrar el login

        else:
            # Si el usuario o la contraseña son incorrectos
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")
            self.pass_entry.delete(0, 'end')
            self.pass_entry.focus()

    def on_dashboard_close(self):
        """Finaliza toda la aplicación si se cierra un dashboard con la 'X'."""
        self.destroy()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()