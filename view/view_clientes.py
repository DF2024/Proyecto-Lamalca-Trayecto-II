# view/view_cliente.py
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Asegura el acceso al paquete controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_cliente import Controlador_cliente

class ClienteView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Clientes")
        self.geometry("900x600")
        
        self.controlador = Controlador_cliente()
        self.id_seleccionado = None  # Para guardar el ID interno del cliente

        self._construir_interfaz()
        self._cargar_clientes()


    
    def _construir_interfaz(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)



        # --- Tabla de Clientes ---
        frame_tabla = ttk.LabelFrame(main_frame, text="Listado de Clientes")
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        columnas = ("ID", "Nombre", "Apellido", "Cédula", "Teléfono", "Dirección")
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

        # --- Formulario de Entrada ---
        frame_form = ttk.LabelFrame(main_frame, text="Datos del Cliente")
        frame_form.pack(pady=10, fill=tk.X)

        # Usamos ttk para un look más moderno y consistente
        tk.Label(frame_form, text="Cédula:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.e_cedula = ttk.Entry(frame_form, width=50)
        self.e_cedula.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.e_nombre = ttk.Entry(frame_form, width=50)
        self.e_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(frame_form, text="Apellido:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.e_apellido = ttk.Entry(frame_form, width=50)
        self.e_apellido.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Teléfono:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.e_telefono = ttk.Entry(frame_form, width=50)
        self.e_telefono.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        tk.Label(frame_form, text="Dirección:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.e_direccion = ttk.Entry(frame_form, width=50)
        self.e_direccion.grid(row=1, column=3, rowspan=2, padx=5, pady=5, sticky="w")

        # --- Botones de Acción ---
        botones_frame = tk.Frame(self)
        botones_frame.pack(pady=10)
        ttk.Button(botones_frame, text="Agregar", command=self._agregar_cliente).grid(row=0, column=0, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Actualizar", command=self._actualizar_cliente).grid(row=0, column=1, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Buscar por Cédula", command=self._buscar_cliente).grid(row=0, column=2, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Eliminar", command=self._eliminar_cliente).grid(row=0, column=3, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Limpiar", command=self._limpiar_entradas).grid(row=0, column=4, padx=10, ipady=4)
        ttk.Button(botones_frame, text="Menú", command=self.volver_al_dashboard).grid(row=0, column=5, padx=10, ipady=4)


    def _cargar_clientes(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            clientes = self.controlador.obtener_todos_los_clientes()
            if clientes:
                for c in clientes:
                    # El modelo devuelve (id, nombre, apellido, cedula, telefono, direccion)
                    self.tabla.insert("", tk.END, values=c)
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Error al cargar los clientes: {e}")

    def _seleccionar_fila(self, event):
        item_seleccionado = self.tabla.focus()
        if item_seleccionado:
            valores = self.tabla.item(item_seleccionado, 'values')
            self._limpiar_entradas()
            
            # El ID es el primer valor (índice 0)
            self.id_seleccionado = valores[0]
            
            # Llenar los campos con los demás valores
            self.e_nombre.insert(0, valores[1])
            self.e_apellido.insert(0, valores[2])
            self.e_cedula.insert(0, valores[3])
            self.e_telefono.insert(0, valores[4])
            self.e_direccion.insert(0, valores[5])
            
            # Deshabilitar el entry de la cédula para evitar que se modifique
            # ya que es nuestra clave para actualizar y eliminar.
            self.e_cedula.config(state="disabled")

    def _limpiar_entradas(self):
        self.e_cedula.config(state="normal") # Habilitar la cédula antes de limpiar
        self.id_seleccionado = None
        self.e_nombre.delete(0, tk.END)
        self.e_apellido.delete(0, tk.END)
        self.e_cedula.delete(0, tk.END)
        self.e_telefono.delete(0, tk.END)
        self.e_direccion.delete(0, tk.END)
        
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])

    def _agregar_cliente(self):
        nombre = self.e_nombre.get().strip()
        apellido = self.e_apellido.get().strip()
        cedula = self.e_cedula.get().strip()
        telefono = self.e_telefono.get().strip()
        direccion = self.e_direccion.get().strip()

        if not all([nombre, apellido, cedula]):
            messagebox.showwarning("Campos Requeridos", "Nombre, Apellido y Cédula son obligatorios.")
            return

        resultado = self.controlador.insertar_cliente(nombre, apellido, cedula, telefono, direccion)
        if resultado:
            messagebox.showinfo("Éxito", "Cliente agregado exitosamente.")
            self._cargar_clientes()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error", "No se pudo agregar el cliente. Es posible que la cédula ya exista.")

    def _actualizar_cliente(self):
        # La cédula se obtiene del campo de texto, que fue llenado al seleccionar
        cedula = self.e_cedula.get().strip()
        if not cedula or self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un cliente de la lista para actualizar.")
            return

        nombre = self.e_nombre.get().strip()
        apellido = self.e_apellido.get().strip()
        telefono = self.e_telefono.get().strip()
        direccion = self.e_direccion.get().strip()

        if not all([nombre, apellido]):
            messagebox.showwarning("Campos Requeridos", "Nombre y Apellido son obligatorios.")
            return

        resultado = self.controlador.actualizar_cliente_por_cedula(nombre, apellido, cedula, telefono, direccion)
        if resultado:
            messagebox.showinfo("Éxito", "Cliente actualizado exitosamente.")
            self._cargar_clientes()
            self._limpiar_entradas()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el cliente.")

    def _buscar_cliente(self):
        cedula = self.e_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Campo Requerido", "Debe ingresar una cédula para buscar.")
            return
            
        cliente = self.controlador.obtener_cliente_por_cedula(cedula)
        if cliente:
            self._limpiar_entradas()
            # Llenamos los campos con los datos encontrados
            self.id_seleccionado = cliente[0]
            self.e_nombre.insert(0, cliente[1])
            self.e_apellido.insert(0, cliente[2])
            self.e_cedula.insert(0, cliente[3])
            self.e_telefono.insert(0, cliente[4])
            self.e_direccion.insert(0, cliente[5])
            self.e_cedula.config(state="disabled")
            messagebox.showinfo("Cliente Encontrado", f"Se han cargado los datos de {cliente[1]} {cliente[2]}.")
        else:
            messagebox.showwarning("No Encontrado", f"No se encontró un cliente con la cédula {cedula}.")

    def _eliminar_cliente(self):
        cedula = self.e_cedula.get().strip()
        if not cedula or self.id_seleccionado is None:
            messagebox.showwarning("Acción Requerida", "Debe seleccionar un cliente de la lista para eliminar.")
            return
            
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al cliente con cédula {cedula}?"):
            resultado = self.controlador.eliminar_cliente_por_cedula(cedula)
            if resultado:
                messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
                self._cargar_clientes()
                self._limpiar_entradas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente. Es posible que esté asociado a una compra.")
    
    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ClienteView(root)
    ventana.mainloop()