# view/view_inventario.py
import tkinter as tk
from tkinter import messagebox, ttk, TclError
from tkcalendar import DateEntry
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
from controller.controller_inventario import Controlador_inventario
from controller.controller_categoria import Controlador_categoria
from controller.controller_proveedor import Controlador_proveedor

class InventarioView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Inventario")
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
        
        # Controladores
        self.controlador_inventario = Controlador_inventario()
        self.controlador_categoria = Controlador_categoria()
        self.controlador_proveedor = Controlador_proveedor()


        # Datos internos
        self.categorias_map = {}
        self.proveedores_map = {}
        self.categorias_map_rev = {}
        self.proveedores_map_rev = {}
        self.id_seleccionado = None
        self.iconos = {}

        if iconos_disponibles:
            self._cargar_iconos()

        self._construir_interfaz()
        self._cargar_comboboxes()
        self._cargar_inventario()

    def _cargar_iconos(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icons")
        if not os.path.isdir(icon_path): return
        icon_files = {
            "add": "add_light.png", "update": "update_light.png", "delete": "delete_light.png",
            "clear": "clear_light.png", "menu": "menu_light.png"
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
        frame_form = ttk.LabelFrame(main_frame, text="Datos del Producto", padding=(15, 10))
        frame_form.pack(pady=10, fill=tk.X)
        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        entry_font = ('Arial', 10)
        # Fila 0
        ttk.Label(frame_form, text="Producto:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.e_producto = ttk.Entry(frame_form, font=entry_font)
        self.e_producto.grid(row=0, column=1, columnspan=3, padx=5, pady=8, sticky="ew")

        # Fila 1
        ttk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.e_cantidad = ttk.Entry(frame_form, font=entry_font)
        self.e_cantidad.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Precio Unitario:").grid(row=1, column=2, padx=(15, 5), pady=8, sticky="w")
        self.e_precio_unitario = ttk.Entry(frame_form, font=entry_font)
        self.e_precio_unitario.grid(row=1, column=3, padx=5, pady=8, sticky="ew")

        # Fila 2
        ttk.Label(frame_form, text="Categoría:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.combo_categoria = ttk.Combobox(frame_form, state="readonly", font=entry_font)
        self.combo_categoria.grid(row=2, column=1, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Proveedor:").grid(row=2, column=2, padx=(15, 5), pady=8, sticky="w")
        self.combo_proveedor = ttk.Combobox(frame_form, state="readonly", font=entry_font)
        self.combo_proveedor.grid(row=2, column=3, padx=5, pady=8, sticky="ew")
        
        # Fila 3
        ttk.Label(frame_form, text="Fecha de Entrada:").grid(row=3, column=0, padx=5, pady=8, sticky="w")
        self.e_fecha = DateEntry(frame_form, date_pattern='yyyy-mm-dd', state="readonly",
                                background=self.entry_bg, foreground=self.fg_color, bordercolor=self.bg_color,
                                headersbackground=self.bg_color, normalbackground=self.entry_bg,
                                weekendbackground=self.entry_bg, othermonthwebackground=self.entry_bg,
                                selectbackground=self.select_bg, font=entry_font)
        self.e_fecha.grid(row=3, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(frame_form, text="Observaciones:").grid(row=3, column=2, padx=(15, 5), pady=8, sticky="w")
        self.e_observaciones = ttk.Entry(frame_form, font=entry_font)
        self.e_observaciones.grid(row=3, column=3, padx=5, pady=8, sticky="ew")

        # --- Frame de Botones de Acción ---
        botones_frame = tk.Frame(main_frame, bg=self.bg_color)
        botones_frame.pack(pady=20)
        btn_params = {'ipadx': 10, 'ipady': 5, 'padx': 8}
        
        ttk.Button(botones_frame, text="Agregar", image=self.iconos.get('add'), compound=tk.LEFT, command=self._agregar_inventario).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Actualizar", image=self.iconos.get('update'), compound=tk.LEFT, command=self._actualizar_inventario).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Eliminar", image=self.iconos.get('delete'), compound=tk.LEFT, command=self._eliminar_inventario).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Limpiar", image=self.iconos.get('clear'), compound=tk.LEFT, command=self._limpiar_entradas).pack(side=tk.LEFT, **btn_params)

        # --- Frame de la Tabla de Inventario ---
        frame_tabla = ttk.LabelFrame(main_frame, text="Inventario Actual", padding=(15, 10))
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        columnas = ("ID", "Producto", "Cantidad", "Precio Unit.", "Fecha Entrada", "Categoría", "Proveedor", "Observaciones")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)
            # Anchos de columna ajustados
            if col == "ID": self.tabla.column(col, width=40, anchor="center")
            elif col == "Observaciones": self.tabla.column(col, width=220)
            elif col == "Producto": self.tabla.column(col, width=180)
            else: self.tabla.column(col, width=100, anchor="center")
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)
        
        ttk.Button(main_frame, text="Volver al Menú Principal", image=self.iconos.get('menu'), compound=tk.LEFT, command=self.volver_al_dashboard).pack(pady=(10,0))

    def _cargar_comboboxes(self):
        try:
            categorias = self.controlador_categoria.obtener_todas_las_categorias()
            nombres_cat = []
            for id_categoria, nombre_categoria in categorias:
                self.categorias_map[nombre_categoria] = id_categoria
                self.categorias_map_rev[id_categoria] = nombre_categoria
                nombres_cat.append(nombre_categoria)
            self.combo_categoria['values'] = nombres_cat

            proveedores = self.controlador_proveedor.obtener_todos_los_proveedores()
            nombres_prov = []
            for prov in proveedores:
                id_proveedor, _, nombre_proveedor = prov[:3]
                self.proveedores_map[nombre_proveedor] = id_proveedor
                self.proveedores_map_rev[id_proveedor] = nombre_proveedor
                nombres_prov.append(nombre_proveedor)
            self.combo_proveedor['values'] = nombres_prov
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los datos de los menús: {e}")

    def _cargar_inventario(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            inventario = self.controlador_inventario.obtener_todo_inventario()
            if inventario:
                for i, item in enumerate(inventario):
                    id_inv, producto, cantidad, precio_unitario, fecha, observaciones, id_categoria, id_proveedor = item
                    nombre_cat = self.categorias_map_rev.get(id_categoria, "N/A")
                    nombre_prov = self.proveedores_map_rev.get(id_proveedor, "N/A")
                    precio_formateado = f"{float(precio_unitario):.2f}" if precio_unitario else "0.00"
                    
                    # El orden de 'values' debe coincidir con el de 'columnas'
                    valores_tabla = (id_inv, producto, cantidad, precio_formateado, fecha, nombre_cat, nombre_prov, observaciones)
                    
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    self.tabla.insert("", tk.END, values=valores_tabla, tags=(tag,))
            
            self.tabla.tag_configure('evenrow', background=self.bg_color)
            self.tabla.tag_configure('oddrow', background=self.entry_bg)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el inventario: {e}")

    def _seleccionar_fila(self, event):
        selected_item = self.tabla.focus()
        if not selected_item: return
        
        valores = self.tabla.item(selected_item, 'values')
        self._limpiar_entradas()
        
        id_inv, producto, cantidad, precio, fecha, categoria, proveedor, observaciones = valores
        
        self.id_seleccionado = id_inv
        self.e_producto.insert(0, producto)
        self.e_cantidad.insert(0, cantidad)
        self.e_precio_unitario.insert(0, precio)
        self.e_fecha.set_date(fecha)
        self.combo_categoria.set(categoria)
        self.e_observaciones.insert(0, observaciones)
        self.combo_proveedor.set(proveedor)

    def _limpiar_entradas(self):
        self.id_seleccionado = None
        for widget in [self.e_producto, self.e_cantidad, self.e_precio_unitario, self.e_observaciones]:
            widget.delete(0, tk.END)
        
        for combo in [self.combo_categoria, self.combo_proveedor]:
            combo.set('')

        try:
            self.e_fecha.set_date(None)
        except Exception:
            pass
        
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
        
        self.e_producto.focus_set()

    def _obtener_datos_formulario(self):
        producto = self.e_producto.get().strip()
        cantidad_str = self.e_cantidad.get().strip()
        precio_str = self.e_precio_unitario.get().strip().replace(',', '.') # Aceptar coma como separador decimal
        
        try:
            fecha = self.e_fecha.get_date()
        except TclError:
            fecha = None
            
        nombre_cat = self.combo_categoria.get()
        observaciones = self.e_observaciones.get().strip()
        nombre_prov = self.combo_proveedor.get()

        campos_obligatorios = [producto, cantidad_str, precio_str, fecha, nombre_cat, nombre_prov]
        if not all(campos_obligatorios):
            messagebox.showwarning("Campos Incompletos", "Todos los campos, excepto observaciones, son obligatorios.")
            return None

        try:
            cantidad_val = int(cantidad_str)
            precio_val = float(precio_str)
            if cantidad_val < 0 or precio_val < 0:
                messagebox.showwarning("Datos Inválidos", "La cantidad y el precio no pueden ser negativos.")
                return None
        except ValueError:
            messagebox.showwarning("Datos Inválidos", "La cantidad debe ser un número entero y el precio un número válido (ej: 19.99).")
            return None

        id_categoria = self.categorias_map.get(nombre_cat)
        if id_categoria is None:
            messagebox.showerror("Error de Datos", f"La categoría '{nombre_cat}' no es válida.")
            return None

        id_proveedor = self.proveedores_map.get(nombre_prov)
        if id_proveedor is None:
            messagebox.showerror("Error de Datos", f"El proveedor '{nombre_prov}' no es válido.")
            return None
        
        return producto, cantidad_val, precio_val, fecha, observaciones, id_categoria, id_proveedor

    def _agregar_inventario(self):
        datos = self._obtener_datos_formulario()
        if not datos: return
        
        producto, cantidad, precio, fecha, observaciones, id_categoria, id_proveedor = datos

        if self.controlador_inventario.verificar_existencia_producto(producto):
            messagebox.showerror("Producto Duplicado", f"El producto '{producto}' ya existe en el inventario.")
            return

        resultado = self.controlador_inventario.insertar_inventario(
            producto, cantidad, precio, fecha, id_categoria, observaciones, id_proveedor
        )
        if resultado:
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            self._cargar_inventario()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error", "No se pudo agregar el producto.")

    def _actualizar_inventario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No Seleccionado", "Por favor, seleccione un producto de la lista.")
            return
            
        datos = self._obtener_datos_formulario()
        if not datos: return
        
        producto, cantidad, precio, fecha, observaciones, id_categoria, id_proveedor = datos

        if self.controlador_inventario.verificar_existencia_producto(producto, self.id_seleccionado):
            messagebox.showerror("Producto Duplicado", f"Ya existe otro producto con el nombre '{producto}'.")
            return

        resultado = self.controlador_inventario.actualizar_inventario(
            self.id_seleccionado, producto, cantidad, precio, fecha, id_categoria, observaciones, id_proveedor
        )
        if resultado:
            messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
            self._cargar_inventario()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el producto.")

    def _eliminar_inventario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No Seleccionado", "Por favor, seleccione un producto de la lista.")
            return
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el producto ID {self.id_seleccionado}?\nEsta acción es irreversible.", icon='warning'):
            resultado = self.controlador_inventario.eliminar_producto(self.id_seleccionado)
            if resultado:
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
                self._cargar_inventario()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto. Puede estar asociado a una venta.")

    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()

# El resto del código `if __name__ == "__main__"` está bien.

if __name__ == "__main__":
    # Mock para pruebas sin base de datos real
    class MockController:
        def obtener_todas_las_categorias(self): return [(1, 'Lácteos'), (2, 'Carnes')]
        def obtener_todos_los_proveedores(self): return [(101, 'J-123', 'Proveedor A'), (102, 'J-456', 'Proveedor B')]
        def obtener_todo_inventario(self): 
            return [
                (1, 'Leche', 50, '2023-10-27', 'Producto frágil', 1, 101),
                (2, 'Queso', 30, '2023-10-26', '', 1, 101),
                (3, 'Pollo', 100, '2023-10-25', 'Congelado', 2, 102)
            ]
        def insertar_inventario(self, *args): print("Insertando:", args); return True
        def actualizar_inventario(self, *args): print("Actualizando:", args); return True
        def eliminar_inventario(self, *args): print("Eliminando:", args); return True

    root = tk.Tk()
    root.withdraw()
    
    # Asignar los mocks a la clase antes de crear la instancia
    InventarioView.controlador_inventario = MockController()
    InventarioView.controlador_producto = MockController()
    InventarioView.controlador_categoria = MockController()
    InventarioView.controlador_proveedor = MockController()
    
    ventana = InventarioView(root)
    ventana.mainloop()