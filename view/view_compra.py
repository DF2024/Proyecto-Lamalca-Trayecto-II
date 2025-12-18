# Archivo: view/view_compra.py (VERSIÓN FINAL Y VERIFICADA)
import tkinter as tk
from tkinter import messagebox, ttk, TclError
import sys
import os
import webbrowser

try:
    from PIL import Image, ImageTk
    iconos_disponibles = True
except ImportError:
    iconos_disponibles = False

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_compra import Controlador_compra
from controller.controller_cliente import Controlador_cliente
from controller.controller_inventario import Controlador_inventario
from controller.controller_cierre_caja import Controlador_cierre_caja

class CompraView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro de Ventas y Carrito de Compras")
        self.controlador_cierre_caja = Controlador_cierre_caja()
        self.geometry("1200x850")

        # --- Estilos ---
        self.bg_color = "#2e2e2e"
        self.fg_color = "#dcdcdc"
        self.entry_bg = "#3c3c3c"
        self.select_bg = "#0078D7"
        self.configure(bg=self.bg_color)
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

        self.controlador_compra = Controlador_compra()
        self.controlador_cliente = Controlador_cliente()
        self.controlador_inventario = Controlador_inventario()
        self.controlador_cierre_caja = Controlador_cierre_caja()

        self.inventario_data = {}
        self.id_cliente_seleccionado = None
        self.iconos = {}
        self.carrito = []

        if iconos_disponibles: self._cargar_iconos()
        self._construir_interfaz()
        self._cargar_productos_combobox()
        self._cargar_compras_tabla()

    def _cargar_iconos(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icons")
        if not os.path.isdir(icon_path): return
        icon_files = { "add": "add_light.png", "remove": "delete_light.png", "search": "search_light.png", "clear": "clear_light.png", "menu": "menu_light.png", "cart": "add_light.png" }
        for name, filename in icon_files.items():
            try:
                path = os.path.join(icon_path, filename)
                image = Image.open(path).resize((16, 16), Image.LANCZOS)
                self.iconos[name] = ImageTk.PhotoImage(image)
            except Exception: self.iconos[name] = None
    
    def _construir_interfaz(self):
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(4, weight=1)
        main_frame.columnconfigure(0, weight=1)

        frame_seleccion = ttk.LabelFrame(main_frame, text="Paso 1: Seleccionar Cliente y Productos", padding=(15, 10))
        frame_seleccion.grid(row=0, column=0, pady=10, sticky="ew") 
        frame_seleccion.columnconfigure(1, weight=1)
        ttk.Label(frame_seleccion, text="Cédula Cliente:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.entry_cedula = ttk.Entry(frame_seleccion, font=('Arial', 10))
        self.entry_cedula.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        ttk.Button(frame_seleccion, text="Buscar", image=self.iconos.get('search'), compound=tk.LEFT, command=self._buscar_cliente).grid(row=0, column=2, padx=5, pady=8)
        self.label_nombre_cliente = ttk.Label(frame_seleccion, text="<-- Busque un cliente", font=('Arial', 10, 'italic'))
        self.label_nombre_cliente.grid(row=0, column=3, columnspan=3, padx=15, pady=8, sticky="w")
        ttk.Label(frame_seleccion, text="Producto:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.combo_producto = ttk.Combobox(frame_seleccion, state="readonly", font=('Arial', 10))
        self.combo_producto.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
        self.combo_producto.bind("<<ComboboxSelected>>", self._actualizar_info_producto)
        ttk.Label(frame_seleccion, text="Cantidad:").grid(row=1, column=2, padx=(15, 5), pady=8, sticky="e")
        self.entry_cantidad = ttk.Entry(frame_seleccion, width=10, font=('Arial', 10))
        self.entry_cantidad.grid(row=1, column=3, padx=5, pady=8, sticky="w")
        ttk.Label(frame_seleccion, text="Stock:").grid(row=1, column=4, padx=5, pady=8, sticky="e")
        self.label_stock = ttk.Label(frame_seleccion, text="0", font=("Arial", 10, "bold"))
        self.label_stock.grid(row=1, column=5, padx=5, pady=8, sticky="w")
        btn_add_cart = ttk.Button(frame_seleccion, text="Añadir al Carrito", image=self.iconos.get('cart'), compound=tk.LEFT, command=self._anadir_al_carrito)
        btn_add_cart.grid(row=1, column=6, padx=15, pady=8, sticky="e")
        frame_seleccion.columnconfigure(6, weight=1)

        frame_carrito = ttk.LabelFrame(main_frame, text="Paso 2: Carrito de Compra", padding=(15, 10))
        frame_carrito.grid(row=1, column=0, pady=10, sticky="nsew") 
        columnas_carrito = ("ID Prod", "Producto", "Cantidad", "Precio Unit.", "Subtotal")
        self.tabla_carrito = ttk.Treeview(frame_carrito, columns=columnas_carrito, show="headings", displaycolumns=("Producto", "Cantidad", "Precio Unit.", "Subtotal"), height=5)
        for col in columnas_carrito:
            if col != "ID Prod": self.tabla_carrito.heading(col, text=col)
        self.tabla_carrito.pack(side="left", fill="both", expand=True)
        scrollbar_carrito = ttk.Scrollbar(frame_carrito, orient="vertical", command=self.tabla_carrito.yview)
        self.tabla_carrito.configure(yscrollcommand=scrollbar_carrito.set)
        scrollbar_carrito.pack(side="right", fill="y")
        
        frame_finalizar = ttk.LabelFrame(main_frame, text="Paso 3: Finalizar Venta", padding=(15, 10))
        frame_finalizar.grid(row=2, column=0, pady=10, sticky="ew")
        frame_finalizar.columnconfigure(3, weight=1)
        ttk.Button(frame_finalizar, text="Remover Producto", image=self.iconos.get('remove'), compound=tk.LEFT, command=self._remover_del_carrito).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_finalizar, text="Limpiar Todo", image=self.iconos.get('clear'), compound=tk.LEFT, command=self._limpiar_formulario).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_finalizar, text="TOTAL A PAGAR:", font=('Arial', 12, 'bold')).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.label_total = ttk.Label(frame_finalizar, text="0.00 Bs.", font=("Arial", 16, "bold"), foreground="#4CAF50")
        self.label_total.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        btn_registrar = ttk.Button(frame_finalizar, text="REGISTRAR VENTA", image=self.iconos.get('add'), compound=tk.LEFT, command=self._registrar_compra)
        btn_registrar.grid(row=0, column=6, padx=15, pady=5, sticky="e")
        frame_finalizar.columnconfigure(6, weight=1)
        
        frame_historial = ttk.LabelFrame(main_frame, text="Historial de Ítems Vendidos", padding=(15, 10))
        frame_historial.grid(row=4, column=0, pady=10, sticky="nsew") 
        columnas_historial = ("ID Venta", "Cédula", "Cliente", "Producto", "Cant.", "Fecha", "Total Ítem")
        self.tabla_compras = ttk.Treeview(frame_historial, columns=columnas_historial, show="headings")
        for col in columnas_historial: self.tabla_compras.heading(col, text=col)
        self.tabla_compras.pack(side="left", fill="both", expand=True)
        scrollbar_historial = ttk.Scrollbar(frame_historial, orient="vertical", command=self.tabla_compras.yview)
        self.tabla_compras.configure(yscrollcommand=scrollbar_historial.set)
        scrollbar_historial.pack(side="right", fill="y")
        
        frame_botones_final = ttk.Frame(main_frame)
        frame_botones_final.grid(row=5, column=0, pady=10, sticky="e")
        ttk.Button(frame_botones_final, text="Volver al Menú Principal", image=self.iconos.get('menu'), compound=tk.LEFT, command=self.volver_al_dashboard).pack()

    def _registrar_compra(self):
        # <<-- VALIDACIÓN DE CAJA ABIERTA
        sesion_abierta = self.controlador_cierre_caja.obtener_estado_caja()
        if not sesion_abierta:
            messagebox.showerror("Caja Cerrada", "No se puede registrar una venta porque no hay una sesión de caja abierta.")
            return

        if not self.id_cliente_seleccionado:
            return messagebox.showerror("Falta Cliente", "Debe buscar y seleccionar un cliente válido.")
        if not self.carrito:
            return messagebox.showerror("Carrito Vacío", "Debe añadir al menos un producto al carrito.")

        id_nueva_compra = self.controlador_compra.registrar_venta_completa(
            id_cliente=self.id_cliente_seleccionado, items_carrito=self.carrito
        )

        if id_nueva_compra:
            messagebox.showinfo("Éxito", f"Venta ID {id_nueva_compra} registrada correctamente.")
            if messagebox.askyesno("Generar Factura", "¿Desea generar la factura para esta venta?"):
                self._generar_y_abrir_factura(id_nueva_compra)
            self._cargar_productos_combobox()
            self._cargar_compras_tabla()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo registrar la venta.")
            
    def _generar_y_abrir_factura(self, id_venta):
        path_pdf, mensaje = self.controlador_compra.generar_factura_venta(id_venta)
        if path_pdf:
            messagebox.showinfo("Factura Generada", f"{mensaje}\nEl archivo se guardó en: {path_pdf}")
            try: webbrowser.open(os.path.realpath(path_pdf))
            except Exception as e: messagebox.showwarning("No se pudo abrir", f"No se pudo abrir el PDF.\nError: {e}")
        else: messagebox.showerror("Error de Factura", mensaje)
            
    def volver_al_dashboard(self):
        self.destroy()
        if self.master: self.master.deiconify()

    def _anadir_al_carrito(self):
        nombre_prod = self.combo_producto.get()
        if not nombre_prod: return messagebox.showerror("Sin Producto", "Por favor, seleccione un producto.")
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0: raise ValueError()
        except (ValueError, TclError): return messagebox.showerror("Cantidad Inválida", "La cantidad debe ser un número entero positivo.")
        id_inventario, datos_prod = next(((i, d) for i, d in self.inventario_data.items() if d['nombre'] == nombre_prod), (None, None))
        if not datos_prod: return
        stock_disponible = datos_prod['stock']
        cantidad_en_carrito = sum(item['cantidad'] for item in self.carrito if item['id_inventario'] == id_inventario)
        if (cantidad + cantidad_en_carrito) > stock_disponible:
            return messagebox.showerror("Stock Insuficiente", f"Stock para '{nombre_prod}' insuficiente.\nDisponible: {stock_disponible} | En carrito: {cantidad_en_carrito}")
        for item in self.carrito:
            if item['id_inventario'] == id_inventario:
                item['cantidad'] += cantidad
                item['subtotal'] = item['cantidad'] * item['precio_unitario']
                break
        else:
            self.carrito.append({'id_inventario': id_inventario, 'nombre': nombre_prod, 'cantidad': cantidad, 'precio_unitario': datos_prod['precio'], 'subtotal': cantidad * datos_prod['precio']})
        self._refrescar_tabla_carrito()
        self.combo_producto.set('')
        self.entry_cantidad.delete(0, 'end')
        self.label_stock.config(text="0")

    def _remover_del_carrito(self):
        item_seleccionado = self.tabla_carrito.focus()
        if not item_seleccionado: return messagebox.showwarning("Sin Selección", "Seleccione un producto del carrito para remover.")
        index_a_remover = self.tabla_carrito.index(item_seleccionado)
        self.carrito.pop(index_a_remover)
        self._refrescar_tabla_carrito()

    def _refrescar_tabla_carrito(self):
        for i in self.tabla_carrito.get_children(): self.tabla_carrito.delete(i)
        total_venta = 0.0
        for item in self.carrito:
            self.tabla_carrito.insert("", "end", values=(item['id_inventario'], item['nombre'], item['cantidad'], f"{item['precio_unitario']:.2f}", f"{item['subtotal']:.2f}"))
            total_venta += item['subtotal']
        self.label_total.config(text=f"{total_venta:.2f} Bs.")

    def _limpiar_formulario(self):
        self.id_cliente_seleccionado = None
        self.entry_cedula.delete(0, "end")
        self.label_nombre_cliente.config(text="<-- Busque un cliente", foreground=self.fg_color, font=('Arial', 10, 'italic'))
        self.combo_producto.set('')
        self.entry_cantidad.delete(0, 'end')
        self.label_stock.config(text="0")
        self.carrito.clear()
        self._refrescar_tabla_carrito()
    
    def _cargar_productos_combobox(self):
        self.inventario_data.clear()
        nombres_prod = []
        try:
            productos_inventario = self.controlador_inventario.obtener_todo_inventario()
            for item in productos_inventario:
                id_inv, nombre, stock, precio_venta = item[0], item[1], item[2], item[3]
                if int(stock) > 0:
                    self.inventario_data[id_inv] = {'nombre': nombre, 'precio': float(precio_venta), 'stock': int(stock)}
                    nombres_prod.append(nombre)
            self.combo_producto['values'] = sorted(nombres_prod)
        except Exception as e: messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")

    def _cargar_compras_tabla(self):
        for item in self.tabla_compras.get_children(): self.tabla_compras.delete(item)
        compras = self.controlador_compra.obtener_todas_las_compras()
        if compras:
            for i, compra in enumerate(compras):
                fecha_formateada = compra['fecha'].strftime('%Y-%m-%d %H:%M')
                valores_tupla = (compra['id_venta'], compra['cedula'], compra['nombre_cliente'], compra['nombre_producto'], compra['cantidad'], fecha_formateada, f"{float(compra['total_linea']):.2f}")
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tabla_compras.insert("", "end", values=valores_tupla, tags=(tag,))
        self.tabla_compras.tag_configure('evenrow', background=self.bg_color)
        self.tabla_compras.tag_configure('oddrow', background=self.entry_bg)
    
    def _buscar_cliente(self):
        cedula = self.entry_cedula.get().strip()
        if not cedula: return
        cliente = self.controlador_cliente.obtener_cliente_por_cedula(cedula)
        if cliente:
            self.id_cliente_seleccionado = cliente[0]
            self.label_nombre_cliente.config(text=f"{cliente[1]} {cliente[2]}", foreground="#4CAF50")
        else:
            self.id_cliente_seleccionado = None
            self.label_nombre_cliente.config(text="Cliente no encontrado.", foreground="#F44336")

    def _actualizar_info_producto(self, *args):
        nombre_prod_sel = self.combo_producto.get()
        if not nombre_prod_sel: return
        for data in self.inventario_data.values():
            if data['nombre'] == nombre_prod_sel:
                self.label_stock.config(text=str(data['stock']))
                break

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = CompraView(root)
    app.mainloop()