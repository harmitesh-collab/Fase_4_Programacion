import random #TODO: Agregado para simular errores aleatorios en la reserva, se eliminará cuando se integre la lógica real

# Conectamos con las clases necesarias para la reserva
from cliente import Cliente
from servicio import Servicio

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
    # 1. Obtenemos la hora exacta del evento
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Abrimos en modo 'a' (para agregar al final)
    with open("errores.log", "a") as archivo:
        # 3. Escribimos la línea con formato profesional
        archivo.write(f"[{ahora}] ERROR: {mensaje}\n")
        
intentos = 0
continuar_programa = True

# TODO: Listas de posibles clientes y servicios para simular diferentes escenarios, se eliminarán cuando se integre la lógica real
nombres = ["Ana", "Luis", "Marta", "Pedro", "Elena"]
apellidos = ["Garcia", "Perez", "Lopez", "Sanchez", "Diaz"]
servicios_disponibles = [
    Servicio("Salas", 5000), 
    Servicio("Equipos",""), 
    Servicio("", 15000),
    Servicio("Asesorias", "dos mil")
]

servicios_fallidos = [] # Lista para almacenar servicios que causaron errores para mostrar en el resumen final

while continuar_programa:
    intentos += 1
    print(f"Intento #{intentos}")
    # TODO:Simulación de datos aleatorios para cada intento, incluyendo casos con datos incompletos y tipos de datos incorrectos. Se eliminarán cuando se integre la lógica real de entrada de datos.
    nombre_elegido = random.choice(nombres)
    apellido_elegido = random.choice(apellidos)
    servicio_elegido = random.choice(servicios_disponibles)
    if nombre_elegido == "" or apellido_elegido == "" or servicio_elegido.tipo == "" or servicio_elegido.precio == "":
        errores += 1
        servicios_fallidos.append(servicio_elegido.tipo) # Guardamos el tipo de servicio que causó el error para mostrarlo al final
        registrar_error(f"Datos incompletos en intento {intentos}: Cliente: {nombre_elegido}, {apellido_elegido}, Servicio: {servicio_elegido.tipo}, Precio: {servicio_elegido.precio}")
        print(f"Error registrado en el log por datos incompletos.")
        continue # Sala a la siguiente iteración sin intentar crear la reserva
    
    elif not isinstance(servicio_elegido.precio, (int, float)):
        errores += 1
        servicios_fallidos.append(servicio_elegido.tipo) # Guardamos el tipo de servicio que causó el error para mostrarlo al final
        registrar_error(f"Tipo de dato invalido para el precio: se esperaba numero pero se recibio {type(servicio_elegido.precio)}")
        print(f"Error registrado en el log por precio no numérico.")
        continue # Salta a la siguiente iteración sin intentar crear la reserva
    # Objetos de prueba para simular la creación de reservas
    cliente_recibido = Cliente(nombre_elegido, apellido_elegido)
    servicio_recibido = Servicio(servicio_elegido.tipo, servicio_elegido.precio)
    
    try:
        # TODO: Cambiar esta línea cuando el compañero 2 integre la lógica de polimorfismo
        # costo = servicio_recibido.calcular_costo() 
        #Calculamos el costo usando el objeto recibido
        # Si 'servicio_recibido' no tiene .precio, aquí saltará al 'except'
        costo = servicio_recibido.precio 
        
        # Creamos la reserva
        nueva_reserva = Reserva(cliente_recibido, servicio_recibido)
        
        # 3. Asignamos el costo y actualizamos el estado
        nueva_reserva.costo_total = costo
        nueva_reserva.estado = "Confirmada"
        
        exitos += 1
        print(f"Éxito: Reserva de {servicio_recibido.tipo} para {cliente_recibido.nombre} {cliente_recibido.apellido}.")

    except Exception as e:
        errores += 1
        registrar_error(f"Error en intento {intentos}: {e}")
        print(f"Error registrado en el log.")

    
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