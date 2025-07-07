# view/view_cliente.py
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import re

# --- Para temas y estilos ---
try:
    from ttkthemes import ThemedTk
    temas_disponibles = True
except ImportError:
    temas_disponibles = False
# -------------------------

# --- Para los iconos ---
try:
    from PIL import Image, ImageTk
    iconos_disponibles = True
except ImportError:
    iconos_disponibles = False
# --------------------

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_cliente import Controlador_cliente

class ClienteView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Clientes")
        self.geometry("1200x750")

        # <<<<<<<<<<<<<<<<<<<< CONFIGURACIÓN DEL TEMA OSCURO >>>>>>>>>>>>>>>>>>>
        self.bg_color = "#2e2e2e"
        self.fg_color = "#dcdcdc"
        self.entry_bg = "#3c3c3c"
        self.entry_fg = "#dcdcdc"
        self.select_bg = "#5c5c5c" # Color de fondo al seleccionar

        # Si ttkthemes está disponible, lo usamos para un look profesional
        if temas_disponibles:
            try:
                # Aplicamos el tema a la ventana principal (Toplevel)
                self.tk.call("source", os.path.join(os.path.dirname(__file__), "themes", "equilux", "equilux.tcl"))
                self.tk.call("set_theme", "dark")
            except tk.TclError:
                # Si falla, usamos un estilo manual
                self.configure(bg=self.bg_color)
                style = ttk.Style(self)
                style.theme_use('clam')
        else:
            self.configure(bg=self.bg_color)
            style = ttk.Style(self)
            style.theme_use('clam')

        # Configuración manual de estilos para unificar la apariencia
        style = ttk.Style(self)
        style.configure(".", background=self.bg_color, foreground=self.fg_color, fieldbackground=self.entry_bg, bordercolor="#555555")
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("TButton", padding=6, relief="flat", background="#4a4a4a", foreground=self.fg_color)
        style.map("TButton",
            background=[('active', '#5a5a5a'), ('pressed', '#6a6a6a')],
            foreground=[('active', 'white')])
        style.configure("Treeview", rowheight=25, fieldbackground=self.entry_bg, background=self.entry_bg, foreground=self.fg_color)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#3c3c3c", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#4c4c4c')])
        style.map("Treeview", background=[('selected', self.select_bg)])
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        self.controlador = Controlador_cliente()
        self.id_seleccionado = None
        self.iconos = {}

        if iconos_disponibles:
            self._cargar_iconos()

        self._construir_interfaz()
        self._cargar_clientes()

    def _cargar_iconos(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icons")
        if not os.path.isdir(icon_path): return

        icon_files = {
            "add": "add_light.png", "update": "update_light.png", "delete": "delete_light.png",
            "search": "search_light.png", "clear": "clear_light.png", "menu": "menu_light.png"
        }
        for name, filename in icon_files.items():
            try:
                path = os.path.join(icon_path, filename)
                image = Image.open(path).resize((16, 16), Image.LANCZOS)
                self.iconos[name] = ImageTk.PhotoImage(image)
            except Exception as e:
                self.iconos[name] = None
    
    def _construir_interfaz(self):
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        frame_form = ttk.LabelFrame(main_frame, text="Datos del Cliente", padding=(15, 10))
        frame_form.pack(pady=10, fill=tk.X)
        frame_form.columnconfigure(1, weight=3)
        frame_form.columnconfigure(3, weight=3)
        
        entry_font = ('Arial', 10)
        # --- Campos del Formulario ---
        ttk.Label(frame_form, text="Cédula:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.e_cedula = ttk.Entry(frame_form, font=entry_font)
        self.e_cedula.grid(row=0, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.e_nombre = ttk.Entry(frame_form, font=entry_font)
        self.e_nombre.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Apellido:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.e_apellido = ttk.Entry(frame_form, font=entry_font)
        self.e_apellido.grid(row=2, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(frame_form, text="Teléfono:").grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.e_telefono = ttk.Entry(frame_form, font=entry_font)
        self.e_telefono.grid(row=0, column=3, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Correo Electrónico:").grid(row=1, column=2, padx=5, pady=8, sticky="w")
        self.e_correo = ttk.Entry(frame_form, font=entry_font)
        self.e_correo.grid(row=1, column=3, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Dirección:").grid(row=2, column=2, padx=5, pady=8, sticky="w")
        self.e_direccion = ttk.Entry(frame_form, font=entry_font)
        self.e_direccion.grid(row=2, column=3, padx=5, pady=8, sticky="ew")
        
        # --- Frame de Botones de Acción ---
        botones_frame = tk.Frame(main_frame, bg=self.bg_color)
        botones_frame.pack(pady=20)
        
        btn_params = {'ipadx': 10, 'ipady': 5, 'padx': 8}
        
        ttk.Button(botones_frame, text="Agregar", image=self.iconos.get('add'), compound=tk.LEFT, command=self._agregar_cliente).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Actualizar", image=self.iconos.get('update'), compound=tk.LEFT, command=self._actualizar_cliente).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Eliminar", image=self.iconos.get('delete'), compound=tk.LEFT, command=self._eliminar_cliente).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Buscar", image=self.iconos.get('search'), compound=tk.LEFT, command=self._buscar_cliente).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Limpiar", image=self.iconos.get('clear'), compound=tk.LEFT, command=self._limpiar_entradas).pack(side=tk.LEFT, **btn_params)
        
        # --- Tabla de Clientes ---
        frame_tabla = ttk.LabelFrame(main_frame, text="Listado de Clientes", padding=(15, 10))
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        columnas = ("ID", "Nombre", "Apellido", "Cédula", "Teléfono", "Correo", "Dirección")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "ID": self.tabla.column(col, width=40, anchor="center")
            elif col == "Dirección": self.tabla.column(col, width=250)
            else: self.tabla.column(col, width=120)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        ttk.Button(main_frame, text="Volver al Menú Principal", image=self.iconos.get('menu'), compound=tk.LEFT, command=self.volver_al_dashboard).pack(pady=(10,0))

    def _cargar_clientes(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            clientes = self.controlador.obtener_todos_los_clientes()
            if clientes:
                for i, c in enumerate(clientes):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    self.tabla.insert("", tk.END, values=c, tags=(tag,))
            # Colores de filas alternados para tema oscuro
            self.tabla.tag_configure('evenrow', background="#2e2e2e", foreground="#dcdcdc")
            self.tabla.tag_configure('oddrow', background="#3c3c3c", foreground="#dcdcdc")
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Error al cargar los clientes: {e}")
    
    # El resto de las funciones (_seleccionar_fila, _limpiar_entradas, _validar_entradas, etc.)
    # no necesitan cambios de color porque usan los estilos ttk que ya hemos configurado.
    # Las pego aquí para que tengas el código completo.
    
    def _seleccionar_fila(self, event):
        item_seleccionado = self.tabla.focus()
        if not item_seleccionado: return
        
        valores = self.tabla.item(item_seleccionado, 'values')
        self._limpiar_entradas()
        
        self.id_seleccionado = valores[0]
        self.e_nombre.insert(0, valores[1])
        self.e_apellido.insert(0, valores[2])
        self.e_cedula.insert(0, valores[3])
        self.e_telefono.insert(0, valores[4])
        self.e_direccion.insert(0, valores[5])
        self.e_correo.insert(0, valores[6])
        
        self.e_cedula.config(state="disabled")

    def _limpiar_entradas(self):
        self.e_cedula.config(state="normal")
        self.id_seleccionado = None
        for entry in [self.e_nombre, self.e_apellido, self.e_cedula, self.e_telefono, self.e_direccion, self.e_correo]:
            entry.delete(0, tk.END)
        
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])

    def _validar_entradas(self):
        nombre = self.e_nombre.get().strip()
        apellido = self.e_apellido.get().strip()
        cedula = self.e_cedula.get().strip()
        telefono = self.e_telefono.get().strip()
        correo = self.e_correo.get().strip()
        
        if not all([nombre, apellido, cedula]):
            messagebox.showwarning("Campos Requeridos", "Nombre, Apellido y Cédula son obligatorios.")
            return None
        
        if not cedula.isdigit() or len(cedula) < 6:
            messagebox.showwarning("Dato Inválido", "La cédula debe contener solo números y tener al menos 6 dígitos.")
            return None
            
        if telefono and not telefono.isdigit():
            messagebox.showwarning("Dato Inválido", "El teléfono debe contener solo números.")
            return None

        if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            messagebox.showwarning("Correo Inválido", "Por favor, ingrese una dirección de correo válida.")
            return None
        return True

    def _agregar_cliente(self):
        if not self._validar_entradas():
            return
            
        cedula = self.e_cedula.get().strip()
        
        if self.controlador.verificar_existencia_cedula(cedula):
            messagebox.showerror("Error de Duplicado", f"La cédula '{cedula}' ya se encuentra registrada.")
            return
        
        nombre = self.e_nombre.get().strip()
        apellido = self.e_apellido.get().strip()
        telefono = self.e_telefono.get().strip()
        direccion = self.e_direccion.get().strip()
        correo = self.e_correo.get().strip()

        resultado = self.controlador.insertar_cliente(nombre, apellido, cedula, telefono, direccion, correo)
        if resultado:
            messagebox.showinfo("Éxito", "Cliente agregado exitosamente.")
            self._cargar_clientes()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo agregar el cliente.")

    def _actualizar_cliente(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un cliente de la lista para actualizar.")
            return
            
        if not self._validar_entradas():
            return

        nombre = self.e_nombre.get().strip()
        apellido = self.e_apellido.get().strip()
        cedula = self.e_cedula.get().strip()
        telefono = self.e_telefono.get().strip()
        direccion = self.e_direccion.get().strip()
        correo = self.e_correo.get().strip()

        resultado = self.controlador.actualizar_cliente_por_cedula(nombre, apellido, cedula, telefono, direccion, correo)
        if resultado:
            messagebox.showinfo("Éxito", "Cliente actualizado exitosamente.")
            self._cargar_clientes()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo actualizar el cliente.")

    def _buscar_cliente(self):
        dialog = tk.Toplevel(self)
        dialog.title("Buscar Cliente")
        dialog.geometry("300x120")
        dialog.configure(bg=self.bg_color)
        
        ttk.Label(dialog, text="Ingrese la Cédula:").pack(pady=10)
        entry_search = ttk.Entry(dialog, width=30)
        entry_search.pack()
        entry_search.focus_set()

        def do_search():
            cedula = entry_search.get().strip()
            dialog.destroy()
            if not cedula: return
            
            cliente = self.controlador.obtener_cliente_por_cedula(cedula)
            if cliente:
                self._limpiar_entradas()
                for item in self.tabla.get_children():
                    if self.tabla.item(item)['values'][3] == cedula:
                        self.tabla.selection_set(item)
                        self.tabla.focus(item)
                        self.tabla.see(item) # Asegura que la fila seleccionada sea visible
                        break
                messagebox.showinfo("Cliente Encontrado", f"Se han cargado los datos de {cliente[1]} {cliente[2]}.")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró un cliente con la cédula {cedula}.")

        btn_frame = tk.Frame(dialog, bg=self.bg_color)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Buscar", command=do_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)
    
    def _eliminar_cliente(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un cliente de la lista para eliminar.")
            return
        
        cedula = self.e_cedula.get().strip()
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al cliente con cédula {cedula}?\nEsta acción no se puede deshacer.", icon='warning'):
            resultado = self.controlador.eliminar_cliente_por_cedula(cedula)
            if resultado:
                messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
                self._cargar_clientes()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.\nEs posible que esté asociado a una venta.")
    
    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ClienteView(root)
    ventana.mainloop()


    