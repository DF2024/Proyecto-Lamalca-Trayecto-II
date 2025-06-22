# view/view_categoria.py

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Asegura que se pueda encontrar el directorio del controlador
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.controller_categoria import Controlador_categoria

class CategoriaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Categorías")
        self.geometry("500x450")
        
        # Ahora se conecta con el controlador REAL
        self.controlador = Controlador_categoria()
        self.id_seleccionado = None

        self._construir_interfaz()
        self._cargar_categorias()

    def _construir_interfaz(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        columnas = ("ID", "Nombre")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        
        self.tabla.heading("ID", text="ID")
        self.tabla.column("ID", width=50, anchor=tk.CENTER)
        
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.column("Nombre", width=350)

        self.tabla.pack(pady=10, fill=tk.BOTH, expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        frame_form = tk.Frame(main_frame)
        frame_form.pack(pady=10, fill=tk.X)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5)
        self.e_nombre = tk.Entry(frame_form, width=40)
        self.e_nombre.grid(row=0, column=1, sticky="ew")

        frame_form.columnconfigure(1, weight=1)

        botones_frame = tk.Frame(main_frame)
        botones_frame.pack(pady=10)

        tk.Button(botones_frame, text="Agregar Categoría", command=self._agregar_categoria).grid(row=0, column=0, padx=5)
        tk.Button(botones_frame, text="Actualizar", command=self._actualizar_categoria).grid(row=0, column=1, padx=5)
        tk.Button(botones_frame, text="Eliminar", command=self._eliminar_categoria).grid(row=0, column=2, padx=5)
        tk.Button(botones_frame, text="Limpiar", command=self._limpiar_entradas).grid(row=0, column=3, padx=5)

    def _limpiar_entradas(self):
        self.e_nombre.delete(0, tk.END)
        self.id_seleccionado = None
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])

    def _cargar_categorias(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        try:
            categorias = self.controlador.obtener_todas_las_categorias()
            if categorias:
                for cat in categorias:
                    self.tabla.insert("", tk.END, values=(cat[0], cat[1]))
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las categorías: {e}")

    def _seleccionar_fila(self, event):
        selected_item = self.tabla.focus()
        if selected_item:
            valores = self.tabla.item(selected_item, 'values')
            self._limpiar_entradas()
            
            self.id_seleccionado = valores[0]
            self.e_nombre.insert(0, valores[1])

    def _agregar_categoria(self):
        nombre = self.e_nombre.get().strip()

        if nombre:
            try:
                resultado = self.controlador.insertar_categoria(nombre)
                if resultado:
                    messagebox.showinfo("Éxito", "Categoría agregada exitosamente.")
                    self._cargar_categorias()
                    self._limpiar_entradas()
                else:
                    messagebox.showerror("Error", "No se pudo agregar la categoría. Es posible que ya exista.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al agregar: {e}")
        else:
            messagebox.showwarning("Campo Vacío", "El nombre de la categoría no puede estar vacío.")

    def _actualizar_categoria(self):
        nombre = self.e_nombre.get().strip()

        if not self.id_seleccionado:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione una categoría de la lista para actualizar.")
            return

        if nombre:
            try:
                resultado = self.controlador.actualizar_categoria(self.id_seleccionado, nombre)
                if resultado:
                    messagebox.showinfo("Éxito", "Categoría actualizada exitosamente.")
                    self._cargar_categorias()
                    self._limpiar_entradas()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la categoría. Es posible que el nuevo nombre ya exista.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al actualizar: {e}")
        else:
            messagebox.showwarning("Campo Vacío", "El nombre de la categoría no puede estar vacío.")

    def _eliminar_categoria(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione una categoría de la lista para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la categoría con ID {self.id_seleccionado}?")
        if confirmar:
            try:
                resultado = self.controlador.eliminar_categoria(self.id_seleccionado)
                if resultado:
                    messagebox.showinfo("Éxito", "Categoría eliminada exitosamente.")
                    self._cargar_categorias()
                    self._limpiar_entradas()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la categoría. Verifique que no esté en uso por algún producto.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

# --- Bloque para probar la ventana de forma independiente ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    ventana_categorias = CategoriaView(root)
    ventana_categorias.mainloop()