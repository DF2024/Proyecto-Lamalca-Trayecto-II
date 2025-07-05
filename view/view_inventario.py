import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
from tkcalendar import DateEntry
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_inventario import Controlador_inventario
from controller.controller_producto import Controlador_producto
from controller.controller_categoria import Controlador_categoria
from controller.controller_proveedor import Controlador_proveedor


class InventarioView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Ingreso de Inventario")
        self.geometry("950x600")


        self.controlador_inventario = Controlador_inventario()
        self.controlador_producto = Controlador_producto()
        self.controlador_categoria = Controlador_categoria()
        self.controlador_proveedor = Controlador_proveedor()


        self.categoria_map = {}
        self.proveedores_map = {}
        self.categoria_map_rev = {}
        self.proveedores_map_rev = {}

        self.id_seleccionado = None

        self._construir_interfaz()
        # self._cargar_comboboxes()
        # self._cargar_inventario()


    def _construir_interfaz(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        frame_tabla = tk.Frame(main_frame)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("ID", "Producto", "Cantidad Actual", "Fecha de Entrada", "Categoria", "Observaciones", "Proveedor")
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

        frame_form = tk.Frame(main_frame)
        frame_form.pack(pady=10, fill=tk.X)

        ### ENTRADAS 

            ##Producto

        tk.Label(frame_form, text="Producto:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.e_producto = ttk.Entry(frame_form, width=40)
        self.e_producto.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

            ##Cantidad

        tk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.e_stock = ttk.Entry(frame_form, width=15)
        self.e_stock.grid(row=1, column=1, padx=5, pady=2, sticky="ew")


            ##Categoria 
        
        tk.Label(frame_form, text="Categoría:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.combo_categoria = ttk.Combobox(frame_form, state="readonly")
        self.combo_categoria.grid(row=2, column=3, padx=5, pady=2, sticky="ew")

            ##Observaciones 

        tk.Label(frame_form, text="Observaciones:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.e_descripcion = ttk.Entry(frame_form, width=40)
        self.e_descripcion.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

            ##Categoria
        
        tk.Label(frame_form, text="Categoria: ").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.combo_categoria = ttk.Combobox(frame_form, state="readonly")
        self.combo_categoria.grid(row=1, column=3, padx=5, pady=2, sticky="ew")

            ##Proveedor

        tk.Label(frame_form, text="Proveedor:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.combo_proveedor = ttk.Combobox(frame_form, state="readonly")
        self.combo_proveedor.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

            ##Fecha
            
        tk.Label(frame_form, text="Fecha:").grid(row=2, column=2, padx=5, pady=2, sticky="w")
        self.entry_fecha = DateEntry(frame_form, date_pattern='yyyy-mm-dd', state="readonly")
        self.entry_fecha.grid(row=2, column=3, padx=5, pady=2, sticky="ew")


        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        ## Botones 

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
            for cat in categorias:
                id_categoria = cat[0]
                nombre_categoria = cat[1]
                self.categorias_map[nombre_categoria] = id_categoria
                self.categorias_map_rev[id_categoria] = nombre_categoria
                nombres_cat.append(nombre_categoria)
            self.combo_categoria['values'] = nombres_cat

            proveedores = self.controlador_proveedor.obtener_todos_los_proveedores()
            nombres_prov = []
            for prov in proveedores:
                # ----- ¡AQUÍ ESTÁ LA CORRECCIÓN! -----
                # Usamos el ID (índice 0) para el valor interno.
                # Usamos el NOMBRE (índice 2) para el valor que se muestra.
                id_proveedor = prov[0]
                nombre_proveedor = prov[2] # Anteriormente podría haber estado usando prov[1] (el RIF)

                self.proveedores_map[nombre_proveedor] = id_proveedor   # 'Proveedor A' -> 101
                self.proveedores_map_rev[id_proveedor] = nombre_proveedor # 101 -> 'Proveedor A'
                
                # Añadimos el nombre a la lista que verá el usuario
                nombres_prov.append(nombre_proveedor)
            
            self.combo_proveedor['values'] = nombres_prov

        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los datos para los menús desplegables: {e}")

    def _cargar_inventario(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            inventario = self.controlador_inventario.obtener_todo_inventario()
            if inventario:
                for i in inventario:
                    nombre_cat = self.categorias_map_rev.get(p[5], "N/A")
                    nombre_prov = self.proveedores_map_rev.get(p[6], "N/A")

                    self.tabla.insert("", tk.END, values=(p[0], p[1], p[2], p[3], p[4], nombre_cat, nombre_prov))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el inventario: {e}")

    def _seleccionar_fila(self, event):
        selected_item = self.tabla.focus()
        if selected_item:
            valores = self.tabla.item(selected_item, 'values')
            self._limpiar_entradas()
            
            self.id_seleccionado = valores[0]
            self.e_producto.insert(0, valores[1])
            self.e_cantidad.insert(0, valores[2])
            self.e_fecha.insert(0, valores[3])
            self.combo_categoria.set(0, valores[4])
            self.e_observaciones.insert(0, valores[5])
            self.combo_proveedor.set(0, valores[6])

    def _limpiar_entradas(self):
            self.id_seleccionado = None
            self.e_producto.delete(0, tk.END)
            self.e_cantidad.delete(0, tk.END)
            self.e_fecha.set_date(None)
            self.combo_categoria.set('')
            self.e_observaciones.delete(0, tk.END)
            self.combo_proveedor.set('')
            if self.tabla.selection():
                self.tabla.selection_remove(self.tabla.selection()[0])
    
    def _agregar_inventario(self):
        datos = self._obtener_datos_formulario()
        if datos:
            producto, cantidad, fecha, observaciones, id_categoria, id_proveedor = datos
            resultado = self.controlador_producto.insertar_producto(producto, cantidad, fecha, observaciones, id_categoria, id_proveedor)
            if resultado:
                messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
                self._cargar_productos()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto.")


    def _obtener_datos_formulario(self):
            producto = self.e_producto.get().strip()
            cantidad = self.e_cantidad.get().strip()
            fecha = self.e_fecha.get_date().strip()
            nombre_cat = self.combo_categoria.get()
            observaciones = self.e_observaciones.get().strip()
            nombre_prov = self.e_combo_proveedor.get()

            if not all([producto, cantidad, fecha, nombre_cat, observaciones, nombre_prov]):
                messagebox.showwarning("Campos incompletos", "Producto, cantidad, fecha, categoria, proveedor son obligatorios.")

            try:
                cantidad_val = int(cantidad)
            except ValueError:
                messagebox.showwarning("Datos inválidos", "La cantidad debe ser un número entero.")

            id_categoria = self.categorias_map.get(nombre_cat)
            id_proveedor = self.proveedores_map.get(nombre_prov)

            return producto, cantidad, fecha, observaciones, id_categoria, id_proveedor

    def _actualizar_inventario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un producto de la lista.")
            return

        datos = self._obtener_datos_formulario()

        if datos:
            producto, cantidad, fecha, observaciones, id_categoria, id_proveedor = datos
            resultado = self.controlador_inventario.actualizar_invetario(self.id_seleccionado, producto, cantidad, fecha, observaciones, id_categoria, id_proveedor)
            if resultado:
                messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
                self._cargar_productos()
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







if __name__ == "__main__":
    
    class MockController:
        def __init__(self, data): self._data = data
        def obtener_todas_las_categorias(self): return self._data
        def obtener_todos_los_proveedores(self): return self._data
        def obtener_todos_los_productos(self): return self._data
        def insertar_inventario(self, *args): print("Insertando:", args); return True
        def actualizar_inventario(self, *args): print("Actualizando:", args); return True
        def eliminar_inventario(self, *args): print("Eliminando:", args); return True

    
    
    root = tk.Tk()
    root.withdraw()
    ventana = InventarioView(root)
    ventana.mainloop()