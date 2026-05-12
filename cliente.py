class Cliente:
    def __init__(self, nombre, apellido):
        # Atributos privados
        self.__nombre = nombre
        self.__apellido = apellido

    # Métodos Getter para acceder a los datos de forma segura
    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido