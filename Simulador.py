#Universidad del valle de Guatemala
#Nombres:
#Oscar Fernando carnet: 20679
#Pablo Gonzalez carnet: 20362
#Hoja de Trabajo 5 algoritmos y estructuras de datos simulaciones con simpy.

import simpy #Importar modulo simpy para realizar la simulacion.
import random #Importar midulo random para poder generar numeros al azar de un intervalo
import statistics

def proceso(env, tiemproceso, nombre, ram, cantRam, ninstrucciones, velocidad, cpu, colaespera):
 
    #Variables para poder realizar el calculo del tiempo en general que tardan los procesos en ser realizados.
    global t
    global tiemp

    # El proceso entra al sistema pero tiene que esperar a que este le asigne memoria ram para empezar.
    yield env.timeout(tiemproceso)
    print('%s. Solicita %d de RAM (Nuevo Proceso)' % (nombre, cantRam))
    # Se guarda el tiempo en el que llego
    tiemp_llegada = env.now

    # Se solicita la  memoria RAM para la iniciacion del proceso.
    yield ram.get(cantRam)
    print('%s. Solicitud aceptada por %d de RAM (Proceso Admitido)' % (nombre, cantRam))
 
    # En esta variable se almacenara el numero de instrucciones finalizadas
    instruccionesf = 0
    
    while instruccionesf < ninstrucciones:
        # Conexion con el resocurce CPU
        with cpu.request() as req:
            yield req
            # Instruccion a realizarse
            if (ninstrucciones - instruccionesf) >= velocidad:
                ejecutadas = velocidad
            else:
                ejecutadas = (ninstrucciones - instruccionesf)
 
            print('%s. CPU ejecutara %d instrucciones. (Proceso Listo)' % (nombre, ejecutadas))

            # Tiempo de instrucciones a ejecutar
            yield env.timeout(ejecutadas/velocidad)   
 
            # Numero total de intrucciones terminadas
            instruccionesf += ejecutadas
            print('%s. CPU (%d/%d) instrucciones completadas. (Proceso Corriendo)' % (nombre, instruccionesf, ninstrucciones))
 
        # Si la decision es 1 wait, si es 2 procedemos a ready
        desicion = random.randint(1,2)
 
        if desicion == 1 and instruccionesf < ninstrucciones:
            #Etapa de espera en la cola.
            with colaespera.request() as cola:
                yield cola
                yield env.timeout(1);              
                print('%s. Realizadas operaciones de entrada/salida. (Proceso Esperando)' % (nombre))

    #Etapa finalizada
    yield ram.put(cantRam)#Se devuelve la memoria Ram
    print('%s. Retorna %d de RAM. (Proceso terminado)' % (nombre, cantRam))
    #Total de tiempo que llevo el proceso
    t += (env.now - tiemp_llegada)
    #Se guarda tiempo en el Array para luego hacer uso de este y hacer los diferentes calculos.
    tiemp.append(env.now - tiemp_llegada) 


velocidad = 1.0   #Velocidad del Procesador
cantidadram = 100 #Cantidad de Memoria RAM
numeroprocesos = 10  # Numero de procesos que se van a realizar.
t = 0.0       #Variable para el tiempo que tarda un proceso.
tiemp=[]      # Array de los Tiempos que nos ayudara a    almacenar los tiempos transcurridos y luego con el calculo de la desviacion estandar.
 

#Se crea el ambiente de simulacion.
env = simpy.Environment()

# Cola de tipo Resource para el CPU 
cpu = simpy.Resource (env, capacity=1)

# Cola de tipo Container para la RAM
ram = simpy.Container(env, cantidadram, cantidadram)

# Cola de tipo Resource Wait para las operaciones I/O
colaespera = simpy.Resource (env, capacity=2) 

# Numero de intervalos
numerointervalos = 10 

# Semilla del random
random.seed(10000)

# Creacion de un for para poder crear el numero de procesos requeridos por la simulacion.
for i in range(numeroprocesos):
    tiemproceso = random.expovariate(1.0 / numerointervalos)
    #Se genera un numero de instrucciones aleatorio
    ninstrucciones = random.randint(1,10)
    #Se genera una cantidad de memoria RAM aleatoria
    cantRam = random.randint(1,10) 
    env.process(proceso(env, tiemproceso, 'Proceso %d' % i, ram, cantRam, ninstrucciones, velocidad, cpu, colaespera))
 
#Se inicial la simulacion 
env.run()
print

# Calculo del tiempo promedio transcurrido
prom = (t/numeroprocesos)

print("\nSe realizaron %d procesos con la cantidad de intervalos de %d" % (numeroprocesos, numerointervalos))
print ("El tiempo promedio de los procesos es: ",prom," segundos")
#Calculo de la desviacion estandar de la simulacion con la ayuda del modulo de statistics
print("La desviacion estandar es: ",statistics.pstdev(tiemp))
