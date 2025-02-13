# Sistema de reservas para un cine

# Listas para almacenar usuarios y empleados registrados
usuarios_registrados = []
empleados_registrados = []

# Clase base Persona
class Persona:
    def __init__(self, nombre, email, telefono):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre} ({self.email})"

# Clase Usuario
class Usuario(Persona):
    def __init__(self, nombre, email, telefono):
        super().__init__(nombre, email, telefono)
        self.reservas = []

    def reservar_asientos(self, funcion, asientos):
        if funcion.reservar_asientos(asientos):
            reserva = Reserva(self, funcion, asientos)
            self.reservas.append(reserva)
            return reserva
        return None

    def ver_reservas(self):
        if not self.reservas:
            return "No tienes reservas."
        return "\n".join([str(reserva) for reserva in self.reservas])

# Clase Empleado
class Empleado(Persona):
    def __init__(self, nombre, email, telefono, rol, salario):
        super().__init__(nombre, email, telefono)
        self.rol = rol
        self.salario = salario

    def agregar_funcion(self, pelicula, sala, hora):
        if self.rol == "Administrador":
            return Funcion(pelicula, sala, hora)
        raise PermissionError("Solo los administradores pueden agregar funciones.")

    def cambiar_rol(self, nuevo_rol):
        self.rol = nuevo_rol
        print(f"El rol de {self.nombre} ha sido cambiado a {nuevo_rol}.")

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

# Clase Sala
class Sala:
    def __init__(self, nombre, capacidad, tipo):
        self.nombre = nombre
        self.capacidad = capacidad
        self.tipo = tipo
        self.asientos_disponibles = set(range(1, capacidad + 1))

    def reservar_asientos(self, asientos):
        if all(asiento in self.asientos_disponibles for asiento in asientos):
            self.asientos_disponibles -= set(asientos)
            return True
        return False

    def __str__(self):
        return f"{self.nombre} ({self.tipo}, Capacidad: {self.capacidad})"

# Clase Película
class Pelicula:
    def __init__(self, titulo, duracion, clasificacion, genero, director):
        self.titulo = titulo
        self.duracion = duracion
        self.clasificacion = clasificacion
        self.genero = genero
        self.director = director

    def __str__(self):
        return f"{self.titulo} ({self.genero}, Dirigida por {self.director})"

# Clase Reserva
class Reserva:
    def __init__(self, usuario, funcion, asientos):
        self.usuario = usuario
        self.funcion = funcion
        self.asientos = asientos

    def __str__(self):
        return f"Reserva de {self.usuario.nombre} para {self.funcion.pelicula.titulo} en {self.funcion.sala.nombre}, Asientos: {self.asientos}"

# Clase Función
class Funcion:
    def __init__(self, pelicula, sala, hora):
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora

    def reservar_asientos(self, asientos):
        return self.sala.reservar_asientos(asientos)

    def __str__(self):
        return f"Función de {self.pelicula.titulo} en {self.sala.nombre} a las {self.hora}"

# Funciones para registrar usuarios y empleados
def registrar_usuario(nombre, email, telefono):
    # Verificar si el usuario ya existe
    for usuario in usuarios_registrados:
        if usuario.email == email:
            print("Error: El usuario ya está registrado.")
            return None
    # Crear y registrar el nuevo usuario
    nuevo_usuario = Usuario(nombre, email, telefono)
    usuarios_registrados.append(nuevo_usuario)
    print(f"Usuario {nombre} registrado exitosamente.")
    return nuevo_usuario

def registrar_empleado(nombre, email, telefono, rol, salario):
    # Verificar si el empleado ya existe
    for empleado in empleados_registrados:
        if empleado.email == email:
            print("Error: El empleado ya está registrado.")
            return None
    # Crear y registrar el nuevo empleado
    nuevo_empleado = Empleado(nombre, email, telefono, rol, salario)
    empleados_registrados.append(nuevo_empleado)
    print(f"Empleado {nombre} registrado exitosamente.")
    return nuevo_empleado

# Ejemplo de uso
if __name__ == "__main__":
    # Registrar usuarios
    usuario1 = registrar_usuario("Juan Perez", "juan@example.com", "123456789")
    usuario2 = registrar_usuario("Maria Lopez", "maria@example.com", "987654321")

    # Registrar empleados
    empleado1 = registrar_empleado("Admin", "admin@cine.com", "111111111", "Taquillero", 2000)
    empleado2 = registrar_empleado("Limpieza", "limpieza@cine.com", "222222222", "Limpieza", 1500)

    # Cambiar el rol de un empleado
    print("\nAntes del cambio de rol:")
    print(empleado1)  # Taquillero

    empleado1.cambiar_rol("Administrador")
    print("\nDespués del cambio de rol:")
    print(empleado1)  # Administrador

    # Crear una película
    pelicula = Pelicula("Inception", 148, "PG-13", "Ciencia Ficción", "Christopher Nolan")

    # Crear una sala
    sala = Sala("Sala 1", 100, "IMAX")

    # Agregar una función (solo un administrador puede hacerlo)
    if empleado1.rol == "Administrador":
        funcion = empleado1.agregar_funcion(pelicula, sala, "20:00")
        print(f"\nFunción agregada: {funcion}")
    else:
        print("No se pudo agregar la función: empleado no válido.")

    # Reservar asientos (solo un usuario registrado puede hacerlo)
    if usuario1 and funcion:
        reserva = usuario1.reservar_asientos(funcion, [1, 2, 3])
        if reserva:
            print(f"\nReserva exitosa: {reserva}")
        else:
            print("No se pudo realizar la reserva.")
    else:
        print("No se pudo realizar la reserva: usuario o función no válidos.")

    # Ver reservas del usuario
    print("\nReservas de Juan Perez:")
    print(usuario1.ver_reservas())