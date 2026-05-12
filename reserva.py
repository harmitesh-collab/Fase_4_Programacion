import random # Usado para la simulación de 10 operaciones

# Conectamos con las clases necesarias para la reserva
from cliente import Cliente
from servicio import Servicio, ReservaSalas, AlquilerEquipos, AsesoriaEspecializada

# Obtenemos la hora del sistema para el log
from datetime import datetime

# Al inicio del programa: vaciamos el log para esta nueva sesión
with open("errores.log", "w") as archivo:
    archivo.write("--- Inicio de nueva sesion de simulacion ---\n")
    
# Inicializamos los contadores de éxitos y errores
exitos = 0
errores = 0

class Reserva:
    def __init__(self, cliente_obj, servicio_obj):
        self.cliente = cliente_obj
        self.servicio = servicio_obj
        self.estado = "Pendiente"  # Estado inicial por defecto
        self.costo_total = 0       # Se calculará después

# Creamos la función para registrar errores en el log      
def registrar_error(mensaje):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Usamos encoding='utf-8' para evitar problemas con tildes
    with open("errores.log", "a", encoding='utf-8') as archivo:
        archivo.write(f"[{ahora}] ERROR: {mensaje}\n")
        archivo.flush() # Para escribir inmediatamente en el archivo sin esperar a que se cierre
        
intentos = 0
continuar_programa = True

# Listas de posibles clientes y servicios para simular diferentes escenarios
nombres = ["Ana", "Luis", "Marta", "Pedro", "Elena"]
apellidos = ["Garcia", "Perez", "Lopez", "Sanchez", "Diaz"]
servicios_disponibles = [
    ReservaSalas(5000, capacidad=15), 
    AlquilerEquipos(precio_diario="error_string"), # Para probar el log de errores
    ReservaSalas(precio_hora="cinco mil"),         # Para probar validación de tipo
    AsesoriaEspecializada(15000, nivel_experto="Avanzado"),
    AlquilerEquipos(2000, incluye_soporte=True)
]

servicios_fallidos = [] # Lista para almacenar servicios que causaron errores para mostrar en el resumen final

while continuar_programa:
    intentos += 1
    print(f"\nIntento #{intentos}")
    
    nombre_elegido = random.choice(nombres)
    apellido_elegido = random.choice(apellidos)
    servicio_elegido = random.choice(servicios_disponibles)

    # Validación de datos incompletos
    if not nombre_elegido or not apellido_elegido or not servicio_elegido.precio_base:
        errores += 1
        servicios_fallidos.append(servicio_elegido.tipo)
        registrar_error(f"Datos incompletos en intento {intentos}")
        continue

    try:
        # Primero validamos (esto lanzará TypeError o ValueError si el dato es malo)
        servicio_elegido.validar_parametros(duracion=2.0)
        
        # Si la validación pasa, calculamos el costo
        costo = servicio_elegido.calcular_costo(duracion=2.0)
        
        # Creamos el objeto cliente y la reserva
        cliente_obj = Cliente(nombre_elegido, apellido_elegido)
        nueva_reserva = Reserva(cliente_obj, servicio_elegido)
        
        exitos += 1
        print(f"Éxito: {servicio_elegido.describir()} para {cliente_obj.nombre} {cliente_obj.apellido}.")

    except Exception as e:
        # Escribimos el error en el log con detalles del intento y el servicio que falló
        errores += 1
        mensaje_error = f"Intento {intentos} fallido ({servicio_elegido.tipo}): {str(e)}"
        registrar_error(mensaje_error)
        servicios_fallidos.append(servicio_elegido.tipo)
        print(f"Error detectado y guardado en log: {e}")
    
    if intentos >= 10:
        while True:
            try:
                opcion = input("¿Desea continuar? (s/n): ").lower().strip()
                
                if not opcion: # Si el usuario solo presionó Enter
                    print("No escribiste nada. Por favor, elige 's' o 'n'.")
                    continue
                    
                if opcion == 's':
                    break # Sale del menú y sigue con la simulación
                elif opcion == 'n':
                    print("Saliendo...")
                    continuar_programa = False # Sale del bucle principal
                    break
                else:
                    print(f"'{opcion}' no es una opción válida.")
                    
            except Exception as e:
                registrar_error(f"Fallo crítico en menú: {e}")
                print("Ocurrió un error inesperado al leer tu respuesta.")
        
# Muestro el resumen de la sesión al finalizar los intentos
print("\n" + "="*30)
print("RESUMEN FINAL DE LA SESIÓN")
print("="*30)
print(f"Operaciones exitosas: {exitos}")
print(f"Errores registrados: {errores}")
print(f"Total de intentos: {intentos}")
if servicios_fallidos:
    print("Servicios que presentaron errores:")
    for servicio in servicios_fallidos:
        print(f"- {servicio}")
print("="*30)