# view/view_compra.py
import tkinter as tk
from tkinter import messagebox, ttk, TclError
from tkcalendar import DateEntry
import sys
import os

# Asegura el acceso a los controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_compra import Controlador_compra
from controller.controller_cliente import Controlador_cliente
from controller.controller_inventario import Controlador_inventario

class CompraView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro de Ventas")
        self.geometry("1100x650") # Un poco más ancho para el stock

        # Controladores
        self.controlador_compra = Controlador_compra()
        self.controlador_cliente = Controlador_cliente()
        self.controlador_inventario = Controlador_inventario()

        # Datos para la lógica interna
        self.inventario_data = {}  # {id_inventario: {'nombre': ..., 'precio': ..., 'stock': ...}}
        self.id_cliente_seleccionado = None
        self.id_compra_seleccionada = None

        self._construir_interfaz()
        self._cargar_productos_combobox()
        self._cargar_compras_tabla()

    def _construir_interfaz(self):
        # --- Frame del Formulario ---
        frame_form = ttk.LabelFrame(self, text="Registrar Nueva Venta")
        frame_form.pack(padx=10, pady=10, fill="x")

        # Fila 1: Cliente
        tk.Label(frame_form, text="Cédula Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_cedula = ttk.Entry(frame_form)
        self.entry_cedula.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(frame_form, text="Buscar Cliente", command=self._buscar_cliente).grid(row=0, column=2, padx=5, pady=5)
        
        self.label_nombre_cliente = ttk.Label(frame_form, text="<-- Ingrese Cédula y presione Buscar", foreground="blue")
        self.label_nombre_cliente.grid(row=0, column=3, columnspan=3, padx=5, pady=5, sticky="w")

        # Fila 2: Producto, Cantidad y Stock
        tk.Label(frame_form, text="Producto:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_producto = ttk.Combobox(frame_form, state="readonly")
        self.combo_producto.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.combo_producto.bind("<<ComboboxSelected>>", self._actualizar_info_producto)

        tk.Label(frame_form, text="Cantidad:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.var_cantidad = tk.StringVar()
        self.var_cantidad.trace_add("write", self._actualizar_total)
        self.entry_cantidad = ttk.Entry(frame_form, textvariable=self.var_cantidad)
        self.entry_cantidad.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Stock Disponible:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.label_stock = ttk.Label(frame_form, text="0", font=("Arial", 10, "bold"))
        self.label_stock.grid(row=1, column=5, padx=5, pady=5, sticky="w")
        
        # Fila 3: Fecha y Total
        tk.Label(frame_form, text="Fecha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_fecha = DateEntry(frame_form, date_pattern='yyyy-mm-dd', state="readonly")
        self.entry_fecha.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_form, text="Total (Bs.):").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.label_total = ttk.Label(frame_form, text="0.00", font=("Arial", 12, "bold"), foreground="green")
        self.label_total.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # Frame de Botones
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Registrar Venta", command=self._registrar_compra).grid(row=0, column=0, padx=10)
        ttk.Button(frame_botones, text="Actualizar Venta", command=self._actualizar_compra).grid(row=0, column=1, padx=10)
        ttk.Button(frame_botones, text="Eliminar Venta", command=self._eliminar_compra).grid(row=0, column=2, padx=10)
        ttk.Button(frame_botones, text="Limpiar", command=self._limpiar_formulario).grid(row=0, column=3, padx=10)
        ttk.Button(frame_botones, text="Menú", command=self.volver_al_dashboard).grid(row=0, column=4, padx=10)

        # Frame de la Tabla de Compras
        frame_tabla = ttk.LabelFrame(self, text="Historial de Ventas")
        frame_tabla.pack(padx=10, pady=10, fill="both", expand=True)
        
        columnas = ("ID", "Cédula", "Cliente", "Producto", "Cant.", "Fecha", "Total", "ID Cliente", "ID Inventario")
        self.tabla_compras = ttk.Treeview(frame_tabla, columns=columnas, show="headings", displaycolumns=("ID", "Cédula", "Cliente", "Producto", "Cant.", "Fecha", "Total"))
        
        for col in self.tabla_compras["columns"]:
            self.tabla_compras.heading(col, text=col)
            if col == "ID": self.tabla_compras.column(col, width=40, anchor="center")
            elif col == "Cliente": self.tabla_compras.column(col, width=200, anchor="center")
            elif col == "Cant.": self.tabla_compras.column(col, width=50, anchor="center")
            else: self.tabla_compras.column(col, width=120, anchor="center")
        
        self.tabla_compras.pack(fill="both", expand=True)
        self.tabla_compras.bind("<<TreeviewSelect>>", self._seleccionar_compra)
    
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
            for compra in compras:
                self.tabla_compras.insert("", "end", values=compra)
    
    def _buscar_cliente(self):
        cedula = self.entry_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Cédula Vacía", "Por favor, ingrese un número de cédula.")
            return
        
        cliente = self.controlador_cliente.obtener_cliente_por_cedula(cedula)
        if cliente:
            self.id_cliente_seleccionado = cliente[0]
            nombre_completo = f"{cliente[1]} {cliente[2]}"
            self.label_nombre_cliente.config(text=f"Cliente: {nombre_completo}", foreground="green")
        else:
            self.id_cliente_seleccionado = None
            self.label_nombre_cliente.config(text="Cliente no encontrado.", foreground="red")

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
        self.label_nombre_cliente.config(text="<-- Ingrese Cédula y presione Buscar", foreground="blue")
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

        resultado = self.controlador_compra.registrar_compra(self.id_cliente_seleccionado, id_inventario, cantidad, fecha, total)
        if resultado:
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            self._cargar_productos_combobox()
            self._cargar_compras_tabla()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo registrar la venta.")
    
    def _seleccionar_compra(self, event):
        item_seleccionado = self.tabla_compras.focus()
        if not item_seleccionado: return
        
        # Obtenemos todos los valores, incluyendo los ocultos
        valores = self.tabla_compras.item(item_seleccionado, 'values')
        
        self.id_compra_seleccionada = valores[0]
        self.entry_cedula.delete(0, "end"); self.entry_cedula.insert(0, valores[1])
        self.label_nombre_cliente.config(text=f"Cliente: {valores[2]}", foreground="green")
        self.combo_producto.set(valores[3])
        self.var_cantidad.set(valores[4])
        self.entry_fecha.set_date(valores[5])
        self.label_total.config(text=valores[6])
        self.id_cliente_seleccionado = valores[7]
        # Actualizamos el label de stock para el producto seleccionado
        self._actualizar_info_producto()
        
    def _actualizar_compra(self):
        if not self.id_compra_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una venta de la lista para actualizar.")
            return
        
        if not self.id_cliente_seleccionado:
            messagebox.showerror("Error", "Debe haber un cliente válido seleccionado.")
            return
            
        nombre_prod_nuevo = self.combo_producto.get()
        id_inventario_nuevo = next((inv_id for inv_id, data in self.inventario_data.items() if data['nombre'] == nombre_prod_nuevo), None)
        if not id_inventario_nuevo:
            messagebox.showerror("Error", "Debe seleccionar un producto válido.")
            return
        
        stock_disponible = self.inventario_data[id_inventario_nuevo]['stock']

        try:
            cantidad_nueva = int(self.var_cantidad.get())
            if cantidad_nueva <= 0: raise ValueError("La cantidad debe ser positiva.")
            
            # Validar stock disponible. Si el producto es el mismo, el stock disponible real
            # es el actual + lo que se va a devolver de la compra original.
            item_original = self.tabla_compras.item(self.tabla_compras.focus(), 'values')
            id_inventario_original = int(item_original[8])
            cantidad_original = int(item_original[4])

            if id_inventario_nuevo == id_inventario_original:
                stock_disponible += cantidad_original

            if cantidad_nueva > stock_disponible:
                messagebox.showerror("Stock Insuficiente", f"No hay suficiente stock. Disponible (considerando devolución): {stock_disponible}")
                return

        except ValueError as e:
            messagebox.showerror("Error de Cantidad", str(e) if str(e) else "La cantidad debe ser un número entero mayor que cero.")
            return
        
        fecha = self.entry_fecha.get_date().strftime('%Y-%m-%d')
        total = float(self.label_total.cget("text"))

        resultado = self.controlador_compra.actualizar_compra(
            self.id_compra_seleccionada, self.id_cliente_seleccionado, id_inventario_nuevo, cantidad_nueva, fecha, total
        )
        if resultado:
            messagebox.showinfo("Éxito", "Venta actualizada correctamente.")
            self._cargar_productos_combobox()
            self._cargar_compras_tabla()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la venta.")

    def _eliminar_compra(self):
        if not self.id_compra_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una venta de la lista para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la venta ID {self.id_compra_seleccionada}?\nEl stock del producto será devuelto al inventario."):
            resultado = self.controlador_compra.eliminar_compra(self.id_compra_seleccionada)
            if resultado:
                messagebox.showinfo("Éxito", "Venta eliminada y stock devuelto.")
                self._cargar_productos_combobox()
                self._cargar_compras_tabla()
                self._limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la venta.")

    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = CompraView(root)
    app.mainloop()