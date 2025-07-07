# view/view_compra.py
import tkinter as tk
from tkinter import messagebox, ttk, TclError
from tkcalendar import DateEntry
import sys
import os
import webbrowser # <-- Para abrir el PDF automáticamente

# --- Dependencias de estilo ---
try:
    from PIL import Image, ImageTk
    iconos_disponibles = True
except ImportError:
    iconos_disponibles = False
# ------------------------------

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_compra import Controlador_compra
from controller.controller_cliente import Controlador_cliente
from controller.controller_inventario import Controlador_inventario

class CompraView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro de Ventas")
        self.geometry("1150x800")

        # --- Paleta de Tema Oscuro ---
        self.bg_color = "#2e2e2e"
        self.fg_color = "#dcdcdc"
        self.entry_bg = "#3c3c3c"
        self.select_bg = "#0078D7"
        self.label_frame_bg = "#3c3c3c"

        self.configure(bg=self.bg_color)
        
        # --- Estilos ttk ---
        style = ttk.Style(self)
        style.theme_use('clam')
        
        style.configure(".", background=self.bg_color, foreground=self.fg_color, fieldbackground=self.entry_bg, bordercolor="#555555")
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("TButton", padding=6, relief="flat", background="#4a4a4a", foreground=self.fg_color, font=('Arial', 10))
        style.map("TButton", background=[('active', '#5a5a5a')])
        style.configure("Treeview", rowheight=25, fieldbackground=self.entry_bg, background=self.entry_bg, foreground=self.fg_color)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#3c3c3c", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#4c4c4c')])
        style.map("Treeview", background=[('selected', self.select_bg)])
        style.configure("TLabelframe", background=self.bg_color, bordercolor="#555555")
        style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.fg_color, font=('Arial', 11, 'bold'))

        # Controladores
        self.controlador_compra = Controlador_compra()
        self.controlador_cliente = Controlador_cliente()
        self.controlador_inventario = Controlador_inventario()

        # Datos internos
        self.inventario_data = {}
        self.id_cliente_seleccionado = None
        self.id_compra_seleccionada = None
        self.iconos = {}

        if iconos_disponibles:
            self._cargar_iconos()

        self._construir_interfaz()
        self._cargar_productos_combobox()
        self._cargar_compras_tabla()

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

        frame_form = ttk.LabelFrame(main_frame, text="Registrar Nueva Venta", padding=(15, 10))
        frame_form.pack(pady=10, fill=tk.X)
        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)
        frame_form.columnconfigure(5, weight=1)

        # Fila 1: Cliente
        ttk.Label(frame_form, text="Cédula Cliente:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.entry_cedula = ttk.Entry(frame_form, font=('Arial', 10))
        self.entry_cedula.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        
        btn_buscar_cliente = ttk.Button(frame_form, text="Buscar", image=self.iconos.get('search'), compound=tk.LEFT, command=self._buscar_cliente)
        btn_buscar_cliente.grid(row=0, column=2, padx=(5, 15), pady=8)
        
        self.label_nombre_cliente = ttk.Label(frame_form, text="<-- Busque un cliente", font=('Arial', 10, 'italic'))
        self.label_nombre_cliente.grid(row=0, column=3, columnspan=3, padx=5, pady=8, sticky="w")

        # Fila 2: Producto, Cantidad y Stock
        ttk.Label(frame_form, text="Producto:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.combo_producto = ttk.Combobox(frame_form, state="readonly", font=('Arial', 10))
        self.combo_producto.grid(row=1, column=1, columnspan=2, padx=5, pady=8, sticky="ew")
        self.combo_producto.bind("<<ComboboxSelected>>", self._actualizar_info_producto)

        ttk.Label(frame_form, text="Cantidad:").grid(row=1, column=3, padx=(15, 5), pady=8, sticky="w")
        self.var_cantidad = tk.StringVar()
        self.var_cantidad.trace_add("write", self._actualizar_total)
        self.entry_cantidad = ttk.Entry(frame_form, textvariable=self.var_cantidad, width=10, font=('Arial', 10))
        self.entry_cantidad.grid(row=1, column=4, padx=5, pady=8, sticky="w")
        
        ttk.Label(frame_form, text="Stock:").grid(row=1, column=5, padx=5, pady=8, sticky="e")
        self.label_stock = ttk.Label(frame_form, text="0", font=("Arial", 10, "bold"))
        self.label_stock.grid(row=1, column=6, padx=5, pady=8, sticky="w")
        
        # Fila 3: Fecha y Total
        ttk.Label(frame_form, text="Fecha:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.entry_fecha = DateEntry(frame_form, date_pattern='yyyy-mm-dd', state="readonly",
                                     background=self.entry_bg, foreground=self.fg_color, bordercolor=self.bg_color,
                                     headersbackground=self.bg_color, normalbackground=self.entry_bg,
                                     weekendbackground=self.entry_bg, othermonthwebackground=self.entry_bg,
                                     selectbackground=self.select_bg)
        self.entry_fecha.grid(row=2, column=1, padx=5, pady=8, sticky="ew")
        
        ttk.Label(frame_form, text="Total Venta (Bs.):", font=('Arial', 10, 'bold')).grid(row=2, column=5, padx=5, pady=8, sticky="e")
        self.label_total = ttk.Label(frame_form, text="0.00", font=("Arial", 14, "bold"), foreground="#4CAF50")
        self.label_total.grid(row=2, column=6, padx=5, pady=8, sticky="w")

        # Frame de Botones de Acción
        botones_frame = tk.Frame(main_frame, bg=self.bg_color)
        botones_frame.pack(pady=20)
        
        btn_params = {'ipadx': 10, 'ipady': 5, 'padx': 8}
        
        ttk.Button(botones_frame, text="Registrar Venta", image=self.iconos.get('add'), compound=tk.LEFT, command=self._registrar_compra).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Actualizar Venta", image=self.iconos.get('update'), compound=tk.LEFT, command=self._actualizar_compra).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Eliminar Venta", image=self.iconos.get('delete'), compound=tk.LEFT, command=self._eliminar_compra).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Limpiar", image=self.iconos.get('clear'), compound=tk.LEFT, command=self._limpiar_formulario).pack(side=tk.LEFT, **btn_params)

        # Frame de la Tabla de Compras
        frame_tabla = ttk.LabelFrame(main_frame, text="Historial de Ventas", padding=(15, 10))
        frame_tabla.pack(pady=10, fill="both", expand=True)
        
        columnas = ("ID", "Cédula", "Cliente", "Producto", "Cant.", "Fecha", "Total", "ID Cliente", "ID Inventario")
        self.tabla_compras = ttk.Treeview(frame_tabla, columns=columnas, show="headings", displaycolumns=("ID", "Cédula", "Cliente", "Producto", "Cant.", "Fecha", "Total"))
        
        for col in self.tabla_compras["columns"]:
            self.tabla_compras.heading(col, text=col)
            if col == "ID": self.tabla_compras.column(col, width=40, anchor="center")
            elif col == "Cliente": self.tabla_compras.column(col, width=200)
            elif col == "Cant.": self.tabla_compras.column(col, width=50, anchor="center")
            else: self.tabla_compras.column(col, width=120, anchor="center")
        
        self.tabla_compras.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_compras.yview)
        self.tabla_compras.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabla_compras.bind("<<TreeviewSelect>>", self._seleccionar_compra)
        
        ttk.Button(main_frame, text="Volver al Menú Principal", image=self.iconos.get('menu'), compound=tk.LEFT, command=self.volver_al_dashboard).pack(pady=10)
    
    def _cargar_productos_combobox(self):
        self.inventario_data.clear()
        nombres_prod = []
        try:
            productos_inventario = self.controlador_inventario.obtener_todo_inventario()
            for item in productos_inventario:
                id_inv, nombre, stock, precio, *_ = item
                if int(stock) > 0:
                    self.inventario_data[id_inv] = {'nombre': nombre, 'precio': float(precio), 'stock': int(stock)}
                    nombres_prod.append(nombre)
            self.combo_producto['values'] = nombres_prod
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos del inventario: {e}")

    def _cargar_compras_tabla(self):
        for item in self.tabla_compras.get_children():
            self.tabla_compras.delete(item)
        compras = self.controlador_compra.obtener_todas_las_compras()
        if compras:
            for i, compra in enumerate(compras):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tabla_compras.insert("", "end", values=compra, tags=(tag,))
        self.tabla_compras.tag_configure('evenrow', background=self.bg_color)
        self.tabla_compras.tag_configure('oddrow', background=self.entry_bg)
    
    def _buscar_cliente(self):
        cedula = self.entry_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Cédula Vacía", "Por favor, ingrese un número de cédula.")
            return
        
        cliente = self.controlador_cliente.obtener_cliente_por_cedula(cedula)
        if cliente:
            self.id_cliente_seleccionado = cliente[0]
            nombre_completo = f"{cliente[1]} {cliente[2]}"
            self.label_nombre_cliente.config(text=f"Cliente: {nombre_completo}", foreground="#4CAF50")
        else:
            self.id_cliente_seleccionado = None
            self.label_nombre_cliente.config(text="Cliente no encontrado.", foreground="#F44336")

    def _actualizar_info_producto(self, *args):
        nombre_prod_sel = self.combo_producto.get()
        if not nombre_prod_sel:
            self.label_stock.config(text="0")
            return

        for data in self.inventario_data.values():
            if data['nombre'] == nombre_prod_sel:
                self.label_stock.config(text=str(data['stock']))
                break
        self._actualizar_total()

    def _actualizar_total(self, *args):
        try:
            nombre_prod_sel = self.combo_producto.get()
            cantidad_str = self.var_cantidad.get()
            if not cantidad_str:
                self.label_total.config(text="0.00")
                return

            cantidad = int(cantidad_str)
            if not nombre_prod_sel or cantidad <= 0:
                self.label_total.config(text="0.00")
                return
            
            precio_unitario = 0.0
            for data in self.inventario_data.values():
                if data['nombre'] == nombre_prod_sel:
                    precio_unitario = data['precio']
                    break
            
            total = precio_unitario * cantidad
            self.label_total.config(text=f"{total:.2f}")

        except (ValueError, TclError):
            self.label_total.config(text="0.00")

    def _limpiar_formulario(self):
        self.id_compra_seleccionada = None
        self.id_cliente_seleccionado = None
        self.entry_cedula.delete(0, "end")
        self.label_nombre_cliente.config(text="<-- Busque un cliente", foreground=self.fg_color, font=('Arial', 10, 'italic'))
        self.combo_producto.set('')
        self.var_cantidad.set('')
        self.label_total.config(text="0.00")
        self.label_stock.config(text="0")
        self.entry_fecha.set_date(None)
        if self.tabla_compras.selection():
            self.tabla_compras.selection_remove(self.tabla_compras.selection()[0])
            
    def _registrar_compra(self):
        if not self.id_cliente_seleccionado:
            messagebox.showerror("Error", "Debe buscar y seleccionar un cliente válido.")
            return
            
        nombre_prod = self.combo_producto.get()
        if not nombre_prod:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return
            
        id_inventario, stock_disponible = None, 0
        for inv_id, data in self.inventario_data.items():
            if data['nombre'] == nombre_prod:
                id_inventario = inv_id
                stock_disponible = data['stock']
                break

        try:
            cantidad = int(self.var_cantidad.get())
            if cantidad <= 0: raise ValueError("La cantidad debe ser positiva.")
            if cantidad > stock_disponible:
                messagebox.showerror("Stock Insuficiente", f"No hay suficiente stock para '{nombre_prod}'.\nDisponible: {stock_disponible}")
                return
        except ValueError as e:
            messagebox.showerror("Error de Cantidad", str(e) if str(e) else "La cantidad debe ser un número entero mayor que cero.")
            return
        
        fecha = self.entry_fecha.get_date().strftime('%Y-%m-%d')
        total = float(self.label_total.cget("text"))

        id_nueva_compra = self.controlador_compra.registrar_compra(
            self.id_cliente_seleccionado, id_inventario, cantidad, fecha, total
        )

        if id_nueva_compra:
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")

            # --- PREGUNTAR PARA GENERAR FACTURA ---
            if messagebox.askyesno("Generar Factura", "¿Desea generar la factura para esta venta?"):
                path_pdf, mensaje = self.controlador_compra.generar_factura_venta(id_nueva_compra)
                if path_pdf:
                    messagebox.showinfo("Factura Generada", f"{mensaje}\nEl archivo se guardó en: {path_pdf}")
                    try:
                        webbrowser.open(os.path.realpath(path_pdf))
                    except Exception as e:
                        messagebox.showwarning("No se pudo abrir", f"No se pudo abrir el PDF automáticamente.\nError: {e}")
                else:
                    messagebox.showerror("Error de Factura", mensaje)
            
            # Limpieza final
            self._cargar_productos_combobox()
            self._cargar_compras_tabla()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo registrar la venta.")
    
    def _seleccionar_compra(self, event):
        item_seleccionado = self.tabla_compras.focus()
        if not item_seleccionado: return
        
        valores = self.tabla_compras.item(item_seleccionado, 'values')
        
        self.id_compra_seleccionada = valores[0]
        self.entry_cedula.delete(0, "end"); self.entry_cedula.insert(0, valores[1])
        self.label_nombre_cliente.config(text=f"Cliente: {valores[2]}", foreground="#4CAF50")
        self.combo_producto.set(valores[3])
        self.var_cantidad.set(valores[4])
        self.entry_fecha.set_date(valores[5])
        self.id_cliente_seleccionado = valores[7]
        self._actualizar_info_producto()
        
    def _actualizar_compra(self):
        # ... (La lógica de esta función se mantiene como en la respuesta anterior) ...
        # ... (Asegúrate de tener la versión robusta que maneja la devolución de stock) ...
        pass

    def _eliminar_compra(self):
        # ... (La lógica de esta función se mantiene como en la respuesta anterior) ...
        # ... (Asegúrate de tener la versión robusta que maneja la devolución de stock) ...
        pass

    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = CompraView(root)
    app.mainloop()