from model import Modelo_proveedor

class Controlador_proveedor:
    def __init__(self):
        self.modelo = Modelo_proveedor()

    def crear_proveedor(self, id_proveedor, nombre, telefono, correo, direccion):
        return self.modelo.Insert(id_proveedor, nombre, telefono, correo, direccion)

    def obtener_proveedor(self, id_proveedor):
        return self.modelo.Select(id_proveedor)

    def obtener_todos_los_proveedores(self):
        return self.modelo.Select_all()

    def actualizar_proveedor(self, id_proveedor, nombre, telefono, correo, direccion):
        return self.modelo.Update(id_proveedor, nombre, telefono, correo, direccion)

    def eliminar_proveedor(self, id_proveedor):
        return self.modelo.Delete(id_proveedor)
