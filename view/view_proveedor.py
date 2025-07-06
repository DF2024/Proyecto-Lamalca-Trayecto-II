# view/view_proveedor.py
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# --- Dependencias de estilo ---
try:
    from PIL import Image, ImageTk
    iconos_disponibles = True
except ImportError:
    iconos_disponibles = False
# ------------------------------

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_proveedor import Controlador_proveedor

class ProveedorView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Proveedores")
        self.geometry("1200x750")

        # --- Paleta de Tema Oscuro ---
        self.bg_color = "#2e2e2e"
        self.fg_color = "#dcdcdc"
        self.entry_bg = "#3c3c3c"
        self.select_bg = "#0078D7"

        self.configure(bg=self.bg_color)
        
        # --- Estilos ttk ---
        style = ttk.Style(self)
        style.theme_use('clam')
        
        style.configure(".", background=self.bg_color, foreground=self.fg_color, fieldbackground=self.entry_bg, bordercolor="#555555")
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=('Arial', 10))
        style.configure("TButton", padding=6, relief="flat", background="#4a4a4a", foreground=self.fg_color, font=('Arial', 10))
        style.map("TButton", background=[('active', '#5a5a5a')])
        style.configure("Treeview", rowheight=25, fieldbackground=self.entry_bg, background=self.entry_bg, foreground=self.fg_color)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#3c3c3c", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#4c4c4c')])
        style.map("Treeview", background=[('selected', self.select_bg)])
        style.configure("TLabelframe", background=self.bg_color, bordercolor="#555555")
        style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.fg_color, font=('Arial', 11, 'bold'))
        
        self.controlador = Controlador_proveedor()
        self.id_seleccionado = None
        self.iconos = {}

        if iconos_disponibles:
            self._cargar_iconos()

        self._construir_interfaz()
        self._cargar_proveedores()
    
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
            except Exception:
                self.iconos[name] = None
    
    def _construir_interfaz(self):
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # --- Frame del Formulario ---
        frame_form = ttk.LabelFrame(main_frame, text="Datos del Proveedor", padding=(15, 10))
        frame_form.pack(pady=10, fill=tk.X)
        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        entry_font = ('Arial', 10)
        
        ttk.Label(frame_form, text="RIF:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.e_rif = ttk.Entry(frame_form, font=entry_font)
        self.e_rif.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Nombre/Razón Social:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.e_nombre = ttk.Entry(frame_form, font=entry_font)
        self.e_nombre.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Teléfono:").grid(row=0, column=2, padx=(15, 5), pady=8, sticky="w")
        self.e_telefono = ttk.Entry(frame_form, font=entry_font)
        self.e_telefono.grid(row=0, column=3, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Dirección:").grid(row=1, column=2, padx=(15, 5), pady=8, sticky="w")
        self.e_direccion = ttk.Entry(frame_form, font=entry_font)
        self.e_direccion.grid(row=1, column=3, padx=5, pady=8, sticky="ew")

        # --- Frame de Botones de Acción ---
        botones_frame = tk.Frame(main_frame, bg=self.bg_color)
        botones_frame.pack(pady=20)
        
        btn_params = {'ipadx': 10, 'ipady': 5, 'padx': 8}
        
        ttk.Button(botones_frame, text="Agregar", image=self.iconos.get('add'), compound=tk.LEFT, command=self._agregar_proveedor).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Actualizar", image=self.iconos.get('update'), compound=tk.LEFT, command=self._actualizar_proveedor).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Eliminar", image=self.iconos.get('delete'), compound=tk.LEFT, command=self._eliminar_proveedor).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Buscar", image=self.iconos.get('search'), compound=tk.LEFT, command=self._buscar_proveedor).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Limpiar", image=self.iconos.get('clear'), compound=tk.LEFT, command=self._limpiar_entradas).pack(side=tk.LEFT, **btn_params)

        # --- Frame de la Tabla de Proveedores ---
        frame_tabla = ttk.LabelFrame(main_frame, text="Listado de Proveedores", padding=(15, 10))
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        columnas = ("ID", "RIF", "Nombre", "Teléfono", "Dirección")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "ID": self.tabla.column(col, width=40, anchor="center")
            elif col == "Dirección": self.tabla.column(col, width=300)
            elif col == "Nombre": self.tabla.column(col, width=200)
            else: self.tabla.column(col, width=120)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        ttk.Button(main_frame, text="Volver al Menú Principal", image=self.iconos.get('menu'), compound=tk.LEFT, command=self.volver_al_dashboard).pack(pady=(10,0))
        
    def _cargar_proveedores(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            proveedores = self.controlador.obtener_todos_los_proveedores()
            if proveedores:
                for i, p in enumerate(proveedores):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    self.tabla.insert("", tk.END, values=p, tags=(tag,))
            self.tabla.tag_configure('evenrow', background=self.bg_color)
            self.tabla.tag_configure('oddrow', background=self.entry_bg)
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Error al cargar los proveedores: {e}")

    def _seleccionar_fila(self, event):
        item_seleccionado = self.tabla.focus()
        if not item_seleccionado: return
        
        valores = self.tabla.item(item_seleccionado, 'values')
        self._limpiar_entradas()
        
        self.id_seleccionado = valores[0]
        self.e_rif.insert(0, valores[1])
        self.e_nombre.insert(0, valores[2])
        self.e_telefono.insert(0, valores[3])
        self.e_direccion.insert(0, valores[4])
        
        self.e_rif.config(state="disabled")

    def _limpiar_entradas(self):
        self.e_rif.config(state="normal")
        self.id_seleccionado = None
        self.e_rif.delete(0, tk.END)
        self.e_nombre.delete(0, tk.END)
        self.e_telefono.delete(0, tk.END)
        self.e_direccion.delete(0, tk.END)
        
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
        self.e_rif.focus_set()

    def _validar_entradas(self):
        rif = self.e_rif.get().strip()
        nombre = self.e_nombre.get().strip()
        telefono = self.e_telefono.get().strip()

        if not all([rif, nombre]):
            messagebox.showwarning("Campos Requeridos", "RIF y Nombre son obligatorios.")
            return None

        # Validación simple para RIF (puede ser más compleja según el país)
        if not (rif.isalnum() and len(rif) > 5):
            messagebox.showwarning("Dato Inválido", "El RIF debe ser alfanumérico y tener al menos 6 caracteres.")
            return None

        if telefono and not telefono.isdigit():
            messagebox.showwarning("Dato Inválido", "El teléfono debe contener solo números.")
            return None
            
        return True

    def _agregar_proveedor(self):
        if not self._validar_entradas(): return

        rif = self.e_rif.get().strip()
        
        # Asumiendo que tienes una función para verificar duplicados en el controlador
        # if self.controlador.verificar_existencia_rif(rif):
        #     messagebox.showerror("Error de Duplicado", f"El RIF '{rif}' ya se encuentra registrado.")
        #     return

        nombre = self.e_nombre.get().strip()
        telefono = self.e_telefono.get().strip()
        direccion = self.e_direccion.get().strip()

        resultado = self.controlador.insertar_proveedor(rif, nombre, telefono, direccion)
        if resultado:
            messagebox.showinfo("Éxito", "Proveedor agregado exitosamente.")
            self._cargar_proveedores()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo agregar el proveedor. Es posible que el RIF ya exista.")

    def _actualizar_proveedor(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un proveedor de la lista para actualizar.")
            return

        # Para actualizar, no validamos el RIF porque está deshabilitado
        nombre = self.e_nombre.get().strip()
        telefono = self.e_telefono.get().strip()
        if not nombre:
            messagebox.showwarning("Campo Requerido", "El nombre es obligatorio.")
            return
        if telefono and not telefono.isdigit():
            messagebox.showwarning("Dato Inválido", "El teléfono debe contener solo números.")
            return None

        rif = self.e_rif.get().strip()
        direccion = self.e_direccion.get().strip()

        resultado = self.controlador.actualizar_proveedor_por_rif(rif, nombre, telefono, direccion)
        if resultado:
            messagebox.showinfo("Éxito", "Proveedor actualizado exitosamente.")
            self._cargar_proveedores()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo actualizar el proveedor.")

    def _buscar_proveedor(self):
        dialog = tk.Toplevel(self)
        dialog.title("Buscar Proveedor por RIF")
        dialog.geometry("300x120")
        dialog.configure(bg=self.bg_color)
        
        ttk.Label(dialog, text="Ingrese el RIF:").pack(pady=10)
        entry_search = ttk.Entry(dialog, width=30)
        entry_search.pack()
        entry_search.focus_set()

        def do_search():
            rif = entry_search.get().strip()
            dialog.destroy()
            if not rif: return
            
            proveedor = self.controlador.obtener_proveedor_por_rif(rif)
            if proveedor:
                self._limpiar_entradas()
                for item in self.tabla.get_children():
                    if self.tabla.item(item)['values'][1] == rif:
                        self.tabla.selection_set(item)
                        self.tabla.focus(item)
                        self.tabla.see(item)
                        break
                messagebox.showinfo("Proveedor Encontrado", f"Se han cargado los datos de {proveedor[2]}.")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró un proveedor con el RIF {rif}.")

        btn_frame = tk.Frame(dialog, bg=self.bg_color)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Buscar", command=do_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)

    def _eliminar_proveedor(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un proveedor de la lista para eliminar.")
            return
            
        rif = self.e_rif.get().strip()
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al proveedor con RIF {rif}?\nEsta acción es irreversible.", icon='warning'):
            resultado = self.controlador.eliminar_proveedor_por_rif(rif)
            if resultado:
                messagebox.showinfo("Éxito", "Proveedor eliminado exitosamente.")
                self._cargar_proveedores()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proveedor.\nEs posible que esté asociado a un producto en el inventario.")

    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ProveedorView(root)
    ventana.mainloop()