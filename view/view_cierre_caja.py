import tkinter as tk
from tkinter import messagebox, ttk, TclError
import sys
import os
from decimal import Decimal, InvalidOperation

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_cierre_caja import Controlador_cierre_caja

class CierreCajaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Apertura y Cierre de Caja")
        self.geometry("600x700")

        # --- Estilos (sin cambios) ---
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
        
        # <<<<<<<<<<<<<<<< CAMBIO 1: GUARDAR EL ESTADO ACTUAL DE LA UI >>>>>>>>>>>>>>>>>>
        self.current_ui_state = None  # Puede ser 'apertura', 'cierre' o None

        # Contenedor principal que NUNCA se destruye
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH, pady=20, padx=20)

        # Vincular el evento de foco para la actualización de datos
        self.bind("<FocusIn>", self.actualizar_vista)
        
        # Carga inicial de la interfaz
        self.actualizar_vista()

    def limpiar_frame_principal(self):
        """Función auxiliar para destruir todos los widgets hijos de un frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def actualizar_vista(self, event=None):
        """
        Lógica central. Decide si debe cambiar toda la UI (apertura <-> cierre)
        o si solo debe actualizar los datos de la UI de cierre ya existente.
        """
        sesion_abierta = self.controlador.obtener_estado_caja()
        nuevo_estado = 'cierre' if sesion_abierta else 'apertura'

        # --- CASO 1: El estado de la caja ha cambiado (de cerrada a abierta, o viceversa) ---
        # En este caso, SÍ es necesario reconstruir la interfaz.
        if nuevo_estado != self.current_ui_state:
            self.limpiar_frame_principal()
            if nuevo_estado == 'cierre':
                self.datos_cierre_actual = self.controlador.preparar_datos_cierre()
                self._construir_interfaz_cierre()
            else:
                self._construir_interfaz_apertura()
            self.current_ui_state = nuevo_estado
        
        # --- CASO 2: El estado no ha cambiado (sigue en 'cierre') ---
        # Solo necesitamos actualizar los números, no reconstruir todo. ESTO EVITA EL PARPADEO.
        elif nuevo_estado == 'cierre':
            self.datos_cierre_actual = self.controlador.preparar_datos_cierre()
            self._actualizar_datos_cierre()

    # --- INTERFAZ DE APERTURA ---
    def _construir_interfaz_apertura(self):
        self.title("Apertura de Caja")
        ttk.Label(self.main_frame, text="Abrir Nueva Caja", style="Header.TLabel").pack(pady=20)
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        ttk.Label(form_frame, text="Monto Inicial (Bs.):", style="Data.TLabel").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.monto_inicial_var = tk.StringVar()
        entry_monto = ttk.Entry(form_frame, textvariable=self.monto_inicial_var, font=('Arial', 12), width=20, justify='right')
        entry_monto.grid(row=0, column=1, padx=10, pady=10)
        entry_monto.focus_set()
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Iniciar Caja", command=self._iniciar_caja, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        ttk.Button(button_frame, text="Volver al Menú", command=self.volver_al_dashboard).pack(side=tk.LEFT, padx=10, ipadx=10)

    def _iniciar_caja(self):
        try:
            monto_str = self.monto_inicial_var.get().replace(',', '.').strip()
            if not monto_str: return messagebox.showerror("Error", "El campo de monto inicial no puede estar vacío.")
            monto = float(monto_str)
            if monto < 0: return messagebox.showerror("Error", "El monto inicial no puede ser negativo.")
        except ValueError: return messagebox.showerror("Error", "Por favor, ingrese un monto inicial válido.")
        
        resultado = self.controlador.iniciar_caja(monto)
        if "Error" in str(resultado):
            messagebox.showerror("Error", resultado)
        else:
            messagebox.showinfo("Éxito", "Caja abierta correctamente.")
            self.actualizar_vista() # Llama a la lógica central para cambiar a la vista de cierre.

    # --- INTERFAZ DE CIERRE ---
    def _construir_interfaz_cierre(self):
        """
        CONSTRUYE la interfaz de cierre. Solo se llama una vez cuando se pasa de 'apertura' a 'cierre'.
        Guarda referencias a los widgets que necesitan ser actualizados.
        """
        self.title("Cierre de Caja")
        ttk.Label(self.main_frame, text="Resumen para Cierre de Caja", style="Header.TLabel").pack(pady=10)
        summary_frame = ttk.LabelFrame(self.main_frame, text="Cálculos del Sistema", padding=15)
        summary_frame.pack(pady=10, fill="x")
        summary_frame.columnconfigure(1, weight=1)
        
        # Guardamos referencias a los widgets que cambiarán de valor
        ttk.Label(summary_frame, text="Monto Inicial:", style="Data.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.lbl_monto_inicial = ttk.Label(summary_frame, text="", style="Data.TLabel")
        self.lbl_monto_inicial.grid(row=0, column=1, sticky="e", pady=5)
        
        ttk.Label(summary_frame, text="Ventas del Periodo:", style="Data.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.lbl_ventas_sistema = ttk.Label(summary_frame, text="", style="Data.TLabel")
        self.lbl_ventas_sistema.grid(row=1, column=1, sticky="e", pady=5)

        ttk.Separator(summary_frame).grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        ttk.Label(summary_frame, text="Total Esperado en Caja:", style="Total.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.lbl_total_esperado = ttk.Label(summary_frame, text="", style="Total.TLabel")
        self.lbl_total_esperado.grid(row=3, column=1, sticky="e", pady=5)

        cierre_frame = ttk.LabelFrame(self.main_frame, text="Conteo Manual", padding=15)
        cierre_frame.pack(pady=10, fill="x")
        cierre_frame.columnconfigure(1, weight=1)
        ttk.Label(cierre_frame, text="Monto Contado (Bs.):", style="Data.TLabel").grid(row=0, column=0, sticky="w", pady=10)
        self.monto_final_var = tk.StringVar()
        self.monto_final_var.trace_add("write", self._calcular_diferencia)
        entry_monto_final = ttk.Entry(cierre_frame, textvariable=self.monto_final_var, font=('Arial', 12), width=20, justify='right')
        entry_monto_final.grid(row=0, column=1, sticky="e", pady=10)
        entry_monto_final.focus_set()
        
        ttk.Label(cierre_frame, text="Diferencia:", style="Data.TLabel").grid(row=1, column=0, sticky="w", pady=10)
        self.label_diferencia = ttk.Label(cierre_frame, text="0.00 Bs.", font=('Arial', 12, 'bold'))
        self.label_diferencia.grid(row=1, column=1, sticky="e", pady=10)
        
        ttk.Label(cierre_frame, text="Observaciones:").grid(row=2, column=0, sticky="nw", pady=10)
        self.text_observaciones = tk.Text(cierre_frame, height=3, bg=self.entry_bg, fg=self.fg_color, insertbackground="white", relief="flat")
        self.text_observaciones.grid(row=2, column=1, sticky="ew", pady=10)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Finalizar y Cerrar Caja", command=self._finalizar_cierre, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        ttk.Button(button_frame, text="Volver al Menú", command=self.volver_al_dashboard).pack(side=tk.LEFT, padx=10, ipadx=10)

        # Llenamos los datos por primera vez
        self._actualizar_datos_cierre()

    def _actualizar_datos_cierre(self):
        """
        ACTUALIZA los datos en la interfaz de cierre ya existente. NO la reconstruye.
        Esta es la función clave para evitar el parpadeo.
        """
        if not self.datos_cierre_actual: return

        self.lbl_monto_inicial.config(text=f"{self.datos_cierre_actual['monto_inicial']:.2f} Bs.")
        self.lbl_ventas_sistema.config(text=f"{self.datos_cierre_actual['ventas_sistema']:.2f} Bs.")
        self.lbl_total_esperado.config(text=f"{self.datos_cierre_actual['total_esperado']:.2f} Bs.")
        self._calcular_diferencia() # Recalcula la diferencia por si el total esperado cambió

    def _calcular_diferencia(self, *args):
        if not self.datos_cierre_actual: return
        try:
            monto_contado_str = self.monto_final_var.get().replace(',', '.')
            monto_contado = Decimal(monto_contado_str) if monto_contado_str else Decimal('0')
            total_esperado = self.datos_cierre_actual['total_esperado']
            diferencia = monto_contado - total_esperado
            color = "#4CAF50" if diferencia >= 0 else "#F44336"
            self.label_diferencia.config(text=f"{diferencia:.2f} Bs.", foreground=color)
        except (InvalidOperation, TclError):
            self.label_diferencia.config(text="---", foreground="orange")

    def _finalizar_cierre(self):
        try:
            monto_final_str = self.monto_final_var.get().replace(',', '.')
            if not monto_final_str:
                messagebox.showerror("Error", "Debe ingresar el monto final contado.")
                return
            monto_final = float(monto_final_str)
        except ValueError:
            messagebox.showerror("Error", "El monto contado no es un número válido.")
            return
        
        observaciones = self.text_observaciones.get("1.0", "end-1c").strip()
        
        # Nos aseguramos de tener los datos más actualizados justo antes de cerrar.
        # La función actualizar_vista() se encarga de llamar a preparar_datos_cierre()
        self.actualizar_vista()

        if not self.datos_cierre_actual:
            messagebox.showerror("Error Crítico", "No se encontraron datos de la sesión de caja para cerrar.")
            return

        if messagebox.askyesno("Confirmar Cierre", "¿Está seguro de que desea continuar?"):
            # <<<<<<<<<<<<<<< ESTA ES LA LLAMADA CORREGIDA Y FINAL >>>>>>>>>>>>>>>
            # Ahora pasamos todos los datos que el controlador necesita.
            # 'ventas_sistema' viene de self.datos_cierre_actual, que se refresca con el foco.
            resultado = self.controlador.finalizar_cierre(
                id_cierre=self.datos_cierre_actual['id_cierre'], 
                ventas_sistema=self.datos_cierre_actual['ventas_sistema'],
                monto_final_contado_float=monto_final, 
                observaciones=observaciones
            )
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

            if resultado:
                messagebox.showinfo("Éxito", "Caja cerrada correctamente.")
                self.actualizar_vista()
            else:
                messagebox.showerror("Error", "No se pudo cerrar la caja.")


    def volver_al_dashboard(self):
        self.destroy()
        if self.master: self.master.deiconify()