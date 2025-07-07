# Archivo: view/view_cierre_caja.py
import tkinter as tk
from tkinter import messagebox, ttk, TclError
import sys
import os
from decimal import Decimal, InvalidOperation # <<-- IMPORTANTE: Importar Decimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_cierre_caja import Controlador_cierre_caja

class CierreCajaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Apertura y Cierre de Caja")
        self.geometry("600x800")

        self.bg_color = "#2e2e2e"
        self.fg_color = "#dcdcdc"
        self.entry_bg = "#3c3c3c"
        self.select_bg = "#0078D7"
        self.configure(bg=self.bg_color)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure(".", background=self.bg_color, foreground=self.fg_color, fieldbackground=self.entry_bg, bordercolor="#555555")
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("Header.TLabel", font=('Arial', 14, 'bold'))
        style.configure("Data.TLabel", font=('Arial', 12))
        style.configure("Total.TLabel", font=('Arial', 14, 'bold'), foreground="#4CAF50")
        style.configure("TButton", padding=8, font=('Arial', 10, 'bold'))
        style.configure("TLabelframe.Label", font=('Arial', 11, 'bold'))

        self.controlador = Controlador_cierre_caja()
        self.datos_cierre_actual = None

        self._determinar_estado_caja()

    def _determinar_estado_caja(self):
        sesion_abierta = self.controlador.obtener_estado_caja()
        if sesion_abierta:
            self._construir_interfaz_cierre()
        else:
            self._construir_interfaz_apertura()

    def _construir_interfaz_apertura(self):
        self.title("Apertura de Caja")
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(frame, text="Abrir Nueva Caja", style="Header.TLabel").pack(pady=20)
        
        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Monto Inicial (Bs.):", style="Data.TLabel").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.monto_inicial_var = tk.StringVar()
        entry_monto = ttk.Entry(form_frame, textvariable=self.monto_inicial_var, font=('Arial', 12), width=20, justify='right')
        entry_monto.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(frame, text="Iniciar Caja", command=self._iniciar_caja, style="TButton").pack(pady=20, ipadx=10)
        
    def _iniciar_caja(self):
        try:
            monto = float(self.monto_inicial_var.get().replace(',', '.'))
            if monto < 0:
                messagebox.showerror("Error", "El monto inicial no puede ser negativo.")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un monto inicial válido.")
            return
            
        resultado = self.controlador.iniciar_caja(monto)
        if resultado is True:
            messagebox.showinfo("Éxito", "Caja abierta correctamente.")
            self.destroy()
        else:
            messagebox.showerror("Error", str(resultado))

    def _construir_interfaz_cierre(self):
        self.title("Cierre de Caja")
        self.datos_cierre_actual = self.controlador.preparar_datos_cierre()
        if not self.datos_cierre_actual:
            messagebox.showerror("Error", "No se pudieron cargar los datos de la sesión abierta.")
            self.destroy()
            return

        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Resumen para Cierre de Caja", style="Header.TLabel").pack(pady=20)
        
        summary_frame = ttk.LabelFrame(frame, text="Cálculos del Sistema", padding=15)
        summary_frame.pack(pady=10, fill="x")
        summary_frame.columnconfigure(1, weight=1)
        
        ttk.Label(summary_frame, text="Monto Inicial:", style="Data.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(summary_frame, text=f"{self.datos_cierre_actual['monto_inicial']:.2f} Bs.", style="Data.TLabel").grid(row=0, column=1, sticky="e", pady=5)
        
        ttk.Label(summary_frame, text="Ventas del Periodo:", style="Data.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(summary_frame, text=f"{self.datos_cierre_actual['ventas_sistema']:.2f} Bs.", style="Data.TLabel").grid(row=1, column=1, sticky="e", pady=5)
        
        ttk.Separator(summary_frame).grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(summary_frame, text="Total Esperado en Caja:", style="Total.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Label(summary_frame, text=f"{self.datos_cierre_actual['total_esperado']:.2f} Bs.", style="Total.TLabel").grid(row=3, column=1, sticky="e", pady=5)

        cierre_frame = ttk.LabelFrame(frame, text="Conteo Manual", padding=15)
        cierre_frame.pack(pady=20, fill="x")
        cierre_frame.columnconfigure(1, weight=1)

        ttk.Label(cierre_frame, text="Monto Contado (Bs.):", style="Data.TLabel").grid(row=0, column=0, sticky="w", pady=10)
        self.monto_final_var = tk.StringVar()
        self.monto_final_var.trace_add("write", self._calcular_diferencia)
        entry_monto_final = ttk.Entry(cierre_frame, textvariable=self.monto_final_var, font=('Arial', 12), width=20, justify='right')
        entry_monto_final.grid(row=0, column=1, sticky="e", pady=10)
        
        ttk.Label(cierre_frame, text="Diferencia:", style="Data.TLabel").grid(row=1, column=0, sticky="w", pady=10)
        self.label_diferencia = ttk.Label(cierre_frame, text="0.00 Bs.", font=('Arial', 12, 'bold'))
        self.label_diferencia.grid(row=1, column=1, sticky="e", pady=10)
        
        ttk.Label(cierre_frame, text="Observaciones:").grid(row=2, column=0, sticky="nw", pady=10)
        self.text_observaciones = tk.Text(cierre_frame, height=3, bg=self.entry_bg, fg=self.fg_color, insertbackground="white", relief="flat")
        self.text_observaciones.grid(row=2, column=1, sticky="ew", pady=10)

        ttk.Button(frame, text="Finalizar y Cerrar Caja", command=self._finalizar_cierre, style="TButton").pack(pady=20, ipadx=10)

    def _calcular_diferencia(self, *args):
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<< ESTA ES LA CORRECCIÓN >>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            # 1. Convertimos la entrada del usuario (string) a un objeto Decimal
            monto_contado_str = self.monto_final_var.get().replace(',', '.')
            if not monto_contado_str: # Si el campo está vacío, reseteamos
                self.label_diferencia.config(text="0.00 Bs.", foreground=self.fg_color)
                return

            monto_contado = Decimal(monto_contado_str)
            
            # 2. total_esperado ya es un objeto Decimal que viene del controlador
            total_esperado = self.datos_cierre_actual['total_esperado']
            
            # 3. La resta ahora es entre dos objetos Decimal
            diferencia = monto_contado - total_esperado
            
            color = "#4CAF50" # Verde (sobrante o exacto)
            if diferencia < 0:
                color = "#F44336" # Rojo (faltante)
            
            self.label_diferencia.config(text=f"{diferencia:.2f} Bs.", foreground=color)
        except (InvalidOperation, TclError):
            # InvalidOperation es para errores de conversión de Decimal
            # TclError es por si el widget se destruye
            self.label_diferencia.config(text="0.00 Bs.", foreground=self.fg_color)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def _finalizar_cierre(self):
        try:
            monto_final = float(self.monto_final_var.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Error", "El monto contado no es un número válido.")
            return

        observaciones = self.text_observaciones.get("1.0", "end-1c").strip()
        
        if messagebox.askyesno("Confirmar Cierre", "¿Está seguro de que desea cerrar la caja con los montos ingresados?"):
            resultado = self.controlador.finalizar_cierre(
                self.datos_cierre_actual['id_cierre'],
                self.datos_cierre_actual['ventas_sistema'],
                monto_final, # El controlador se encarga de convertirlo a Decimal
                observaciones
            )
            if resultado:
                messagebox.showinfo("Éxito", "Caja cerrada correctamente.")
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo cerrar la caja.")

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = CierreCajaView(root)
    app.mainloop()