import tkinter as tk
from tkinter import messagebox
from view.admin_dashboard import AdminDashboard
from view.empleado_dashboard import EmpleadoDashboard

# Usuarios simulados (en una app real, esto vendría de la base de datos)
USUARIOS = {
    'admin': {'password': 'admin123', 'rol': 'admin'},
    'empleado': {'password': 'empleado123', 'rol': 'empleado'}
}

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistema Ferretería")
        self.geometry("350x200")
        self._construir_interfaz()

    def _construir_interfaz(self):
        tk.Label(self, text="Usuario").pack(pady=5)
        self.usuario_entry = tk.Entry(self)
        self.usuario_entry.pack(pady=5)

        tk.Label(self, text="Contraseña").pack(pady=5)
        self.contra_entry = tk.Entry(self, show="*")
        self.contra_entry.pack(pady=5)

        tk.Button(self, text="Iniciar sesión", command=self._login).pack(pady=10)

    def _login(self):
        usuario = self.usuario_entry.get()
        clave = self.contra_entry.get()

        if usuario in USUARIOS and USUARIOS[usuario]['password'] == clave:
            self.destroy()  # Cierra la ventana de login
            rol = USUARIOS[usuario]['rol']
            if rol == 'admin':
                AdminDashboard().mainloop()
            elif rol == 'empleado':
                EmpleadoDashboard().mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

if __name__ == '__main__':
    app = LoginView()
    app.mainloop()