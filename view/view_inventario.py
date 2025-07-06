# Archivo: InventarioView.py
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
from tkcalendar import DateEntry

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_inventario import Controlador_inventario
from controller.controller_categoria import Controlador_categoria
from controller.controller_proveedor import Controlador_proveedor

class InventarioView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Inventario")
        self.geometry("950x600")

        self.controlador_inventario = Controlador_inventario()
        self.controlador_categoria = Controlador_categoria()
        self.controlador_proveedor = Controlador_proveedor()

        self.categorias_map = {}
        self.proveedores_map = {}
        self.categorias_map_rev = {}
        self.proveedores_map_rev = {}
        self.id_seleccionado = None

        self._construir_interfaz()
        self._cargar_comboboxes()
        self._cargar_inventario()

    def _construir_interfaz(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        frame_tabla = tk.Frame(main_frame)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columnas = ("ID", "Producto", "Cantidad", "Fecha Entrada", "Categoría", "Observaciones", "Proveedor")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "ID": self.tabla.column(col, width=40, anchor=tk.CENTER)
            elif col == "Observaciones": self.tabla.column(col, width=200)
            elif col == "Producto": self.tabla.column(col, width=150)
            else: self.tabla.column(col, width=100, anchor=tk.CENTER)
        
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        frame_form = ttk.LabelFrame(main_frame, text="Datos del Producto")
        frame_form.pack(pady=10, fill=tk.X)

        tk.Label(frame_form, text="Producto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.e_producto = ttk.Entry(frame_form, width=40)
        self.e_producto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame_form, text="Observaciones:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.e_observaciones = ttk.Entry(frame_form, width=40)
        self.e_observaciones.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.e_cantidad = ttk.Entry(frame_form)
        self.e_cantidad.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_form, text="Categoría:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.combo_categoria = ttk.Combobox(frame_form, state="readonly")
        self.combo_categoria.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(frame_form, text="Proveedor:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_proveedor = ttk.Combobox(frame_form, state="readonly")
        self.combo_proveedor.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame_form, text="Fecha:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.e_fecha = DateEntry(frame_form, date_pattern='yyyy-mm-dd', state="readonly")
        self.e_fecha.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        botones_frame = tk.Frame(main_frame)
        botones_frame.pack(pady=10)
        ttk.Button(botones_frame, text="Agregar", command=self._agregar_inventario).grid(row=0, column=0, padx=10)
        ttk.Button(botones_frame, text="Actualizar", command=self._actualizar_inventario).grid(row=0, column=1, padx=10)
        ttk.Button(botones_frame, text="Eliminar", command=self._eliminar_inventario).grid(row=0, column=2, padx=10)
        ttk.Button(botones_frame, text="Limpiar", command=self._limpiar_entradas).grid(row=0, column=3, padx=10)
        ttk.Button(botones_frame, text="Menú", command=self.volver_al_dashboard).grid(row=0, column=4, padx=10)

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
                for item in inventario:
                    id_inv, producto, cantidad, fecha, observaciones, id_categoria, id_proveedor = item
                    nombre_cat = self.categorias_map_rev.get(id_categoria, "N/A")
                    nombre_prov = self.proveedores_map_rev.get(id_proveedor, "N/A")
                    self.tabla.insert("", tk.END, values=(id_inv, producto, cantidad, fecha, nombre_cat, observaciones, nombre_prov))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el inventario: {e}")

    def _seleccionar_fila(self, event):
        selected_item = self.tabla.focus()
        if selected_item:
            valores = self.tabla.item(selected_item, 'values')
            self._limpiar_entradas()
            
            id_inv, producto, cantidad, fecha, categoria, observaciones, proveedor = valores
            
            self.id_seleccionado = id_inv
            self.e_producto.insert(0, producto)
            self.e_cantidad.insert(0, cantidad)
            self.e_fecha.set_date(fecha)
            self.combo_categoria.set(categoria)
            self.e_observaciones.insert(0, observaciones)
            self.combo_proveedor.set(proveedor)

    def _limpiar_entradas(self):
        self.id_seleccionado = None
        self.e_producto.delete(0, tk.END)
        self.e_cantidad.delete(0, tk.END)
        try:
            self.e_fecha.set_date(None)
        except Exception:
            pass
        self.combo_categoria.set('')
        self.e_observaciones.delete(0, tk.END)
        self.combo_proveedor.set('')
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
    
    def _obtener_datos_formulario(self):
        producto = self.e_producto.get().strip()
        cantidad_str = self.e_cantidad.get().strip()
        
        try:
            fecha = self.e_fecha.get_date()
        except tk.TclError:
            fecha = None
            
        nombre_cat = self.combo_categoria.get()
        observaciones = self.e_observaciones.get().strip()
        nombre_prov = self.combo_proveedor.get()

        campos_obligatorios = [producto, cantidad_str, fecha, nombre_cat, nombre_prov]
        if not all(campos_obligatorios):
            messagebox.showwarning("Campos incompletos", "Todos los campos, excepto observaciones, son obligatorios.")
            return None

        try:
            cantidad_val = int(cantidad_str)
            if cantidad_val < 0:
                messagebox.showwarning("Datos inválidos", "La cantidad no puede ser negativa.")
                return None
        except ValueError:
            messagebox.showwarning("Datos inválidos", "La cantidad debe ser un número entero.")
            return None

        id_categoria = self.categorias_map.get(nombre_cat)
        if id_categoria is None:
            messagebox.showerror("Error de datos", f"La categoría '{nombre_cat}' no es válida.")
            return None

        id_proveedor = self.proveedores_map.get(nombre_prov)
        if id_proveedor is None:
            messagebox.showerror("Error de datos", f"El proveedor '{nombre_prov}' no es válido.")
            return None

        return producto, cantidad_val, fecha, observaciones, id_categoria, id_proveedor

    def _agregar_inventario(self):
        datos = self._obtener_datos_formulario()
        if datos:
            producto, cantidad, fecha, observaciones, id_categoria, id_proveedor = datos


            if self.controlador_inventario.verificar_existencia_producto(producto):
                messagebox.showerror("Error de Duplicado", f"El producto '{producto}' ya se encuentra registrado.")
                return 

            resultado = self.controlador_inventario.insertar_inventario(
                producto, cantidad, fecha, id_categoria, observaciones, id_proveedor
            )
            
            if resultado:
                messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
                self._cargar_inventario()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto.")

    def _actualizar_inventario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un producto de la lista.")
            return
        datos = self._obtener_datos_formulario()
        if datos:
            producto, cantidad, fecha, observaciones, id_categoria, id_proveedor = datos
            
            # <<<<<<<<<<<<<<<<<<<< ESTA ES LA CORRECCIÓN MÁS IMPORTANTE >>>>>>>>>>>>>>>>>>>>>>
            # La llamada al controlador ahora coincide con la firma del método en el controlador.
            # Pasamos `id_categoria` al parámetro `categoria` y `observaciones` al parámetro `observaciones`.
            resultado = self.controlador_inventario.actualizar_inventario(
                self.id_seleccionado, producto, cantidad, fecha, id_categoria, observaciones, id_proveedor
            )
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            
            if resultado:
                messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
                self._cargar_inventario()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto.")

    def _eliminar_inventario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un producto de la lista.")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto ID {self.id_seleccionado}?"):
            resultado = self.controlador_inventario.eliminar_inventario(self.id_seleccionado)
            if resultado:
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
                self._cargar_inventario()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")

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