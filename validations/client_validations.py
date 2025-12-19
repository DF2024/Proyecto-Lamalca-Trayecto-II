import re 

def validar_cliente(data: dict) -> list[str]:
    errores = []

    if not data["nombre"]:
        errores.append("El nombre es obligatorio")

    if not data["apellido"]:
        errores.append("El apellido es obligatorio")

    if not data["cedula"]:
        errores.append("La cédula es obligatoria")
    elif not data["cedula"].isdigit() or len(data["cedula"]) < 6:
        errores.append("La cédula debe tener al menos 6 dígitos numéricos")

    if data["telefono"] and not data["telefono"].isdigit():
        errores.append("El teléfono solo debe contener números")

    if data["correo"] and not re.match(r"[^@]+@[^@]+\.[^@]+", data["correo"]):
        errores.append("El correo electrónico no es válido")

    return errores