# view/view_proveedor.py
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_proveedor import Controlador_proveedor

class ProveedorView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Proveedores")
        self.geometry("900x600")
        
        self.controlador = Controlador_proveedor()
        self.id_seleccionado = None  # Para guardar el ID interno del proveedor

        self._construir_interfaz()
        self._cargar_proveedores()

    def _construir_interfaz(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # --- Tabla de Proveedores ---
        frame_tabla = ttk.LabelFrame(main_frame, text="Listado de Proveedores")
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        columnas = ("ID", "RIF", "Nombre", "Teléfono", "Dirección")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "ID": self.tabla.column(col, width=40, anchor="center")
            elif col == "Dirección": self.tabla.column(col, width=250)
            else: self.tabla.column(col, width=150)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        # --- Formulario de Entrada ---
        frame_form = ttk.LabelFrame(main_frame, text="Datos del Proveedor")
        frame_form.pack(pady=10, fill=tk.X)

        tk.Label(frame_form, text="RIF:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.e_rif = ttk.Entry(frame_form, width=40)
        self.e_rif.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.e_nombre = ttk.Entry(frame_form, width=40)
        self.e_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(frame_form, text="Teléfono:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.e_telefono = ttk.Entry(frame_form, width=40)
        self.e_telefono.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        tk.Label(frame_form, text="Dirección:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.e_direccion = ttk.Entry(frame_form, width=40)
        self.e_direccion.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # --- Botones de Acción ---
        botones_frame = tk.Frame(self)
        botones_frame.pack(pady=10)
        ttk.Button(botones_frame, text="Agregar", command=self._agregar_proveedor).grid(row=0, column=0, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Actualizar", command=self._actualizar_proveedor).grid(row=0, column=1, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Buscar por RIF", command=self._buscar_proveedor).grid(row=0, column=2, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Eliminar", command=self._eliminar_proveedor).grid(row=0, column=3, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Limpiar", command=self._limpiar_entradas).grid(row=0, column=4, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Menú", command=self.volver_al_dashboard).grid(row=0, column=5, padx=10, ipady=4)



    def _cargar_proveedores(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            proveedores = self.controlador.obtener_todos_los_proveedores()
            if proveedores:
                for p in proveedores:
                    self.tabla.insert("", tk.END, values=p)
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Error al cargar los proveedores: {e}")

    def _seleccionar_fila(self, event):
        item_seleccionado = self.tabla.focus()
        if item_seleccionado:
            valores = self.tabla.item(item_seleccionado, 'values')
            self._limpiar_entradas()
            
            self.id_seleccionado = valores[0]
            self.e_rif.insert(0, valores[1])
            self.e_nombre.insert(0, valores[2])
            self.e_telefono.insert(0, valores[3])
            self.e_direccion.insert(0, valores[4])
            
            # Deshabilitar el RIF para evitar que se modifique
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

    def _agregar_proveedor(self):
        rif = self.e_rif.get().strip()
        nombre = self.e_nombre.get().strip()
        telefono = self.e_telefono.get().strip()
        direccion = self.e_direccion.get().strip()

        if not all([rif, nombre]):
            messagebox.showwarning("Campos Requeridos", "RIF y Nombre son obligatorios.")
            return

        resultado = self.controlador.insertar_proveedor(rif, nombre, telefono, direccion)
        if resultado:
            messagebox.showinfo("Éxito", "Proveedor agregado exitosamente.")
            self._cargar_proveedores()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error", "No se pudo agregar el proveedor. Es posible que el RIF ya exista.")

    def _actualizar_proveedor(self):
        rif = self.e_rif.get().strip()
        if not rif or self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un proveedor de la lista para actualizar.")
            return

        nombre = self.e_nombre.get().strip()
        telefono = self.e_telefono.get().strip()
        direccion = self.e_direccion.get().strip()

        if not nombre:
            messagebox.showwarning("Campo Requerido", "El nombre es obligatorio.")
            return

        resultado = self.controlador.actualizar_proveedor_por_rif(rif, nombre, telefono, direccion)
        if resultado:
            messagebox.showinfo("Éxito", "Proveedor actualizado exitosamente.")
            self._cargar_proveedores()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el proveedor.")

    def _buscar_proveedor(self):
        rif = self.e_rif.get().strip()
        if not rif:
            messagebox.showwarning("Campo Requerido", "Debe ingresar un RIF para buscar.")
            return
            
        proveedor = self.controlador.obtener_proveedor_por_rif(rif)
        if proveedor:
            self._limpiar_entradas()
            self.id_seleccionado = proveedor[0]
            self.e_rif.insert(0, proveedor[1])
            self.e_nombre.insert(0, proveedor[2])
            self.e_telefono.insert(0, proveedor[3])
            self.e_direccion.insert(0, proveedor[4])
            self.e_rif.config(state="disabled")
            messagebox.showinfo("Proveedor Encontrado", f"Se han cargado los datos de {proveedor[2]}.")
        else:
            messagebox.showwarning("No Encontrado", f"No se encontró un proveedor con el RIF {rif}.")

    def _eliminar_proveedor(self):
        rif = self.e_rif.get().strip()
        if not rif or self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un proveedor de la lista para eliminar.")
            return
            
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al proveedor con RIF {rif}?"):
            resultado = self.controlador.eliminar_proveedor_por_rif(rif)
            if resultado:
                messagebox.showinfo("Éxito", "Proveedor eliminado exitosamente.")
                self._cargar_proveedores()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proveedor. Es posible que esté asociado a un producto.")

    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ProveedorView(root)
    ventana.mainloop()