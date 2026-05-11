from abc import ABC, abstractmethod

class Servicio(ABC):
    """Clase abstracta base para todos los servicios"""
    
    def __init__(self, tipo: str, precio_base, descripcion: str = ""):
        self.tipo = tipo
        self.precio_base = precio_base
        self.descripcion = descripcion
    
    @abstractmethod
    def calcular_costo(self, duracion: float = 1.0, aplicar_iva: bool = False, descuento: float = 0.0, **kwargs) -> float:
        pass
    
    @abstractmethod
    def describir(self) -> str:
        pass
    
    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        pass


class ReservaSalas(Servicio):
    def __init__(self, precio_hora, capacidad: int = 10):
        super().__init__("Salas", precio_hora, "Sala equipada para reuniones")
        self.capacidad = capacidad
    
    def validar_parametros(self, duracion: float = 1.0, **kwargs):
        if not isinstance(self.precio_base, (int, float)):
            raise TypeError(f"El precio debe ser numérico, se recibió: {type(self.precio_base)}")
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a 0 horas")
        return True
    
    def calcular_costo(self, duracion: float = 1.0, aplicar_iva: bool = False, descuento: float = 0.0, **kwargs) -> float:
        self.validar_parametros(duracion=duracion)
        costo = self.precio_base * duracion
        if aplicar_iva:
            costo *= 1.19
        costo *= (1 - descuento)
        return round(costo, 2)
    
    def describir(self) -> str:
        return f"{self.tipo} | Capacidad: {self.capacidad} personas | ${self.precio_base}/h"


class AlquilerEquipos(Servicio):
    def __init__(self, precio_diario, incluye_soporte: bool = False):
        super().__init__("Equipos", precio_diario, "Equipos tecnológicos")
        self.incluye_soporte = incluye_soporte
    
    def validar_parametros(self, duracion: float = 1.0, **kwargs):
        if not isinstance(self.precio_base, (int, float)):
            raise TypeError(f"El precio debe ser numérico, se recibió: {type(self.precio_base)}")
        if duracion < 0.5:
            raise ValueError("El alquiler mínimo es 0.5 días")
        return True
    
    def calcular_costo(self, duracion: float = 1.0, aplicar_iva: bool = False, descuento: float = 0.0, **kwargs) -> float:
        self.validar_parametros(duracion=duracion)
        costo = self.precio_base * duracion
        if self.incluye_soporte:
            costo *= 1.05
        if aplicar_iva:
            costo *= 1.19
        costo *= (1 - descuento)
        return round(costo, 2)
    
    def describir(self) -> str:
        soporte = "Con soporte" if self.incluye_soporte else "Sin soporte"
        return f"{self.tipo} | ${self.precio_base}/día | {soporte}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, precio_sesion, nivel_experto: str = "Intermedio"):
        super().__init__("Asesorias", precio_sesion, "Consultoría personalizada")
        self.nivel_experto = nivel_experto
        self.multiplicador_nivel = {"Básico": 1.0, "Intermedio": 1.5, "Avanzado": 2.0}.get(nivel_experto, 1.0)
    
    def validar_parametros(self, duracion: float = 1.0, **kwargs):
        if not isinstance(self.precio_base, (int, float)):
            raise TypeError(f"El precio debe ser numérico, se recibió: {type(self.precio_base)}")
        if duracion < 1.0:
            raise ValueError("Las asesorías requieren mínimo 1 hora")
        return True
    
    def calcular_costo(self, duracion: float = 1.0, aplicar_iva: bool = False, descuento: float = 0.0, **kwargs) -> float:
        self.validar_parametros(duracion=duracion)
        costo = self.precio_base * duracion * self.multiplicador_nivel
        if aplicar_iva:
            costo *= 1.19
        costo *= (1 - descuento)
        return round(costo, 2)
    
    def describir(self) -> str:
        return f"{self.tipo} | Nivel: {self.nivel_experto} | ${self.precio_base}/h"
