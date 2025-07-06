# view/view_categoria.py
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
from controller.controller_categoria import Controlador_categoria

class CategoriaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Categorías")
        self.geometry("600x800") # Tamaño ajustado para la simplicidad

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
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("TButton", padding=6, relief="flat", background="#4a4a4a", foreground=self.fg_color, font=('Arial', 10))
        style.map("TButton", background=[('active', '#5a5a5a')])
        style.configure("Treeview", rowheight=25, fieldbackground=self.entry_bg, background=self.entry_bg, foreground=self.fg_color)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#3c3c3c", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#4c4c4c')])
        style.map("Treeview", background=[('selected', self.select_bg)])
        style.configure("TLabelframe", background=self.bg_color, bordercolor="#555555")
        style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.fg_color, font=('Arial', 11, 'bold'))

        self.controlador = Controlador_categoria()
        self.id_seleccionado = None
        self.iconos = {}

        if iconos_disponibles:
            self._cargar_iconos()

        self._construir_interfaz()
        self._cargar_categorias()

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
        frame_form = ttk.LabelFrame(main_frame, text="Nueva/Editar Categoría", padding=(15, 10))
        frame_form.pack(pady=10, fill=tk.X)
        frame_form.columnconfigure(1, weight=1)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.e_nombre = ttk.Entry(frame_form, width=40, font=('Arial', 10))
        self.e_nombre.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # --- Frame de Botones de Acción ---
        botones_frame = tk.Frame(main_frame, bg=self.bg_color)
        botones_frame.pack(pady=20)
        
        btn_params = {'ipadx': 10, 'ipady': 5, 'padx': 8}
        
        ttk.Button(botones_frame, text="Agregar", image=self.iconos.get('add'), compound=tk.LEFT, command=self._agregar_categoria).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Actualizar", image=self.iconos.get('update'), compound=tk.LEFT, command=self._actualizar_categoria).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Eliminar", image=self.iconos.get('delete'), compound=tk.LEFT, command=self._eliminar_categoria).pack(side=tk.LEFT, **btn_params)
        ttk.Button(botones_frame, text="Limpiar", image=self.iconos.get('clear'), compound=tk.LEFT, command=self._limpiar_entradas).pack(side=tk.LEFT, **btn_params)
        
        # --- Frame de la Tabla de Categorías ---
        frame_tabla = ttk.LabelFrame(main_frame, text="Categorías Existentes", padding=(15, 10))
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

        columnas = ("ID", "Nombre")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        self.tabla.heading("ID", text="ID")
        self.tabla.column("ID", width=50, anchor=tk.CENTER)
        
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.column("Nombre", width=350)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)


        # Botón para volver al menú, más discreto
        tk.Frame(main_frame, height=10, bg=self.bg_color).pack() # Espaciador
        ttk.Button(main_frame, text="Volver al Menú Principal", image=self.iconos.get('menu'), compound=tk.LEFT, command=self.volver_al_dashboard).pack(pady=10)

    def _limpiar_entradas(self):
        self.e_nombre.delete(0, tk.END)
        self.id_seleccionado = None
        # Deseleccionar la fila en la tabla para un feedback visual claro
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
        self.e_nombre.focus_set()

    def _cargar_categorias(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        try:
            categorias = self.controlador.obtener_todas_las_categorias()
            if categorias:
                for i, cat in enumerate(categorias):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    self.tabla.insert("", tk.END, values=(cat[0], cat[1]), tags=(tag,))
            # Configurar colores de filas alternados
            self.tabla.tag_configure('evenrow', background=self.bg_color)
            self.tabla.tag_configure('oddrow', background=self.entry_bg)
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las categorías: {e}")

    def _seleccionar_fila(self, event):
        selected_item = self.tabla.focus()
        if selected_item:
            valores = self.tabla.item(selected_item, 'values')
            self.e_nombre.delete(0, tk.END) # Limpiamos antes de insertar
            
            self.id_seleccionado = valores[0]
            self.e_nombre.insert(0, valores[1])

    def _agregar_categoria(self):
        nombre = self.e_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Campo Vacío", "El nombre de la categoría no puede estar vacío.")
            return

        # Podríamos añadir una validación de duplicados aquí si tu controlador la tuviera
        # if self.controlador.verificar_existencia_categoria(nombre):
        #     messagebox.showerror("Error de Duplicado", f"La categoría '{nombre}' ya existe.")
        #     return

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

    def _actualizar_categoria(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione una categoría de la lista para actualizar.")
            return

        nombre = self.e_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Campo Vacío", "El nombre de la categoría no puede estar vacío.")
            return

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

    def _eliminar_categoria(self):
        if not self.id_seleccionado:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione una categoría de la lista para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la categoría con ID {self.id_seleccionado}?\n\nEsta acción no se puede deshacer.", icon='warning'):
            try:
                resultado = self.controlador.eliminar_categoria(self.id_seleccionado)
                if resultado:
                    messagebox.showinfo("Éxito", "Categoría eliminada exitosamente.")
                    self._cargar_categorias()
                    self._limpiar_entradas()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la categoría.\nVerifique que no esté en uso por algún producto en el inventario.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    def volver_al_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()

# --- Bloque para probar la ventana de forma independiente ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    ventana_categorias = CategoriaView(root)
    ventana_categorias.mainloop()