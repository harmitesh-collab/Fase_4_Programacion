class Cliente:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    def mostrar_datos(self):
        print(f"Cliente: {self.nombre}")
        print(f"Cédula: {self.cedula}")


cliente1 = Cliente("Camilo", "12345")
cliente1.mostrar_datos()