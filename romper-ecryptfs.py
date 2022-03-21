#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto es un script para tratar de romper un passphrase de ecryptfs usando fuerza bruta.

import sys
import pexpect
import datetime
import math
import xmlrpc.server
import xmlrpc.client

config = {
    "ecryptcomm": "ecryptfs-unwrap-passphrase",
    "temppassphrase": "/tmp/wrapped-passphrase-temp"
}

inicio = None
final = None
cantcp = 10   # Cantidad de combinaciones probadas por punto.
cantpr = 100  # Cantidad de pruebas por reporte.
cantpp = 1000 # Cantidad de pruebas por paquete.

pizarron = [] # El pizarrón para llevar el estado de los trabajos.
partes = []   # La lista de las partes.
contfichpassph = None # El contenido del ficher passphrase.
roto = False  # Indica si ya logramos romper el passphrase.
maxtp = datetime.timedelta(seconds = 60 * 10) # El tiempo máximo que se va a esperar un paquete.
conti = [0]   # El contador inicial.

def probarPalabra(fichpassph, palabra):
    global config
    # print("Probando \"{}\"".format(palabra))
    expdor = pexpect.spawn("{0} {1}" .format(config["ecryptcomm"], fichpassph))
    expdor.expect("Passphrase: ")
    expdor.sendline(palabra)
    resp = expdor.expect(["Error: ", "[a-z0-9]{10,}"])
    if resp == 0:
        # print("Falló la palabra \"{}\"".format(palabra))
        return False
    else:
        # print("La clave \"{}\" fue exitosa.".format(palabra))
        return True

def ataque_diccionario(fichpassph, fuente):
    print("Haciendo el ataque del diccionario")
    # Lee el diccionario.
    roto = False
    with open(fuente, "r") as fich:
        # Prueba cada palabra en el diccionario.
        for linea in fich:
            palabra = linea[:-1].strip()
            roto = probarPalabra(fichpassph, palabra.capitalize())
            if roto:
                print("Entcontré el passphrase la palabra \"{}\"!!".format(palabra))
                break
            roto = probarPalabra(fichpassph, palabra.upper())
            if roto:
                print("Entcontré el passphrase la palabra \"{}\"!!".format(palabra))
                break
            roto = probarPalabra(fichpassph, palabra.lower())
            if roto:
                print("Encontré el passphrase la palabra \"{}\"!!".format(palabra))
                break
        else:
            print("Se probaron todas las palabras disponibles"
                  + " y no se ha podido romper el passphrase")

def lee_partes(fuente):
    partes = []
    with open(fuente, "r") as hfuente:
        # Pon todas las lineas de fuente en partes.
        for linea in hfuente:
            valor = linea[:-1].strip().lower()
            partes.append(valor)
    return partes

def elimina_repeticiones(partes):
    cont = 0
    seg = 0
    while cont < len(partes):
        seg = cont + 1
        while seg < len(partes):
            if partes[cont] == partes[seg]:
                del(partes[seg])
            else:
                seg += 1
        cont += 1

def sumarle_decimal_contador(contador, base, decimal):
    cont = len(contador) - 1
    while (contador[cont] + decimal) >= base:
        decimal += contador[cont]
        contador[cont] = decimal % base
        decimal = decimal // base
        if (decimal > 0) and (cont == 0):
            contador.insert(cont, 0)
        elif (decimal > 0):
            cont -= 1
    contador[cont] += decimal

def completa_ceros(contador, n):
    contador = ([0] * (n - len(contador))) + contador
    return contador

def verificar_menor(conta, contb):
    if len(conta) > len(contb):
        contb = completa_ceros(contb, len(conta))
    elif len(contb) > len(conta):
        conta = completa_ceros(conta, len(contb))
    return conta < contb

def lee_fichpassph(fichpassph):
    with open(fichpassph, "rb") as hfich:
        return hfich.read()

def servir_partes():
    global partes
    print("Sirviendo partes ...")
    return partes

def servir_fichpassph():
    global contfichpassph
    print("Sirviendo fichpassph ...")
    return xmlrpc.client.Binary(contfichpassph)

def servir_trabajo():
    global pizarron, cantpp, conti, partes, maxtp, roto
    base = len(partes)
    contisel = None
    contfsel = None
    contfante = None
    tpaquete = None
    print("Sirviendo trabajo ...")
    # Verifica si ya fue roto el passphrase, si lo fue no hay que
    # seguir dando trabajos.
    if roto:
        tpaquete = None
    # Verifica el pizarrón
    elif (pizarron == None) or (len(pizarron) == 0):
        # Si el pizarrón está vacío registra el primer trabajo.
        contisel = conti
        contfsel = conti.copy()
        sumarle_decimal_contador(contfsel, base, cantpp)
        tpaquete = [contisel, contfsel, datetime.datetime.now(), 1]
        pizarron.append(tpaquete)
    else:
        # Sino, si el pizarrón ya existe, ya tiene trabajos,
        # verificalo en busca de trabajos.
        for paquete in pizarron:
            if (paquete[3] == 1) and ((datetime.datetime.now() - paquete[2]) > maxtp):
                # Si encuentras un trabajo que ya se le pasó el tiempo, tomalo.
                paquete[2] = datetime.datetime.now()
                tpaquete = paquete
            elif (contfante != None) and (restar_contador(paquete[0], contfante) > 0):
                # Sino, si encuentras un espacio entre 2 trabajos, tomalo.
                contisel = contfante
                contfsel = contfante.copy()
                tam_esp = restar_contador(paquete[0], contfante)
                if tam_esp >= cantpp:
                    tam_esp = cantpp
                sumarle_decimal_contador(contfsel, base, tam_esp)
                tpaquete = [contisel, contfsel, datetime.datetime.now(), 1]
        else:
            # Sino, agrega uno nuevo al final.
            contisel = pizarron[-1][1]
            contfsel = pizarron[-1][1].copy()
            sumarle_decimal_contador(contfsel, base, cantpp)
            tpaquete = [contisel, contfsel, datetime.datetime.now(), 1]
        pizarron.append(tpaquete)
    print("Sirviendo {}.".format(tpaquete))
    return tpaquete

def servir_avisar_final(paquete):
    global pizarron
    i = 0
    print("Recibiendo aviso de final ...")
    # Recorre los trabajos en el pizarrón
    while i < len(pizarron):
        # Si aparece el trabajo que acaba de terminar ponlo en 0
        if paquete[0] == pizarron[i][0]:
            pizarron[i][3] = 0
        # Si hay un trabajo previo en el pizarron, también terminado
        # concatenalos en uno solo para marcar que ese intervalo ya se
        # reviso.
        if ((i > 0) and (pizarron[i - 1][1] == pizarron[i][0])
            and (pizarron[i][3] == 0) and (pizarron[i - 1][3] == pizarron[i][3])):
            pizarron[i - 1][1] = pizarron[i][1]
            del(pizarron[i])
        else:
            i += 1
    return 0

def servir_avisar_roto(contador):
    global roto, partes
    roto = True
    print("Recibiendo aviso de passphrase roto ...")
    combinacion = armar_combinacion(partes, contador)
    print("Encontré el passphrase, es la palabra \"{}\", la combinacion {}."
          .format(combinacion, contador))

def administrar_servidor(fichpassph, fuente, conti):
    global pizarron, partes, contfichpassph, cantpp, roto
    print("Iniciando servidor")
    partes = lee_partes(fuente)
    elimina_repeticiones(partes)
    contfichpassph = lee_fichpassph(fichpassph)
    # pizarron = leer_pizarron()
    with xmlrpc.server.SimpleXMLRPCServer(("localhost", 8080)) as servidor:
        servidor.register_introspection_functions()
        servidor.register_function(servir_partes)
        servidor.register_function(servir_fichpassph)
        servidor.register_function(servir_trabajo)
        servidor.register_function(servir_avisar_final)
        servidor.register_function(servir_avisar_roto)
        servidor.serve_forever()

def recibir_fichero(servicio, contfichero):
    global config
    with open(config["temppassphrase"], "wb") as hfichero:
        hfichero.write(contfichero.data)

def administrar_cliente(url):
    global config
    roto = False
    cont = []
    with xmlrpc.client.ServerProxy(url) as servicio:
        partes = servicio.servir_partes()
        contfichero = servicio.servir_fichpassph()
        recibir_fichero(servicio, contfichero)
        while not roto:
            trabajo = servicio.servir_trabajo()
            if trabajo == None:
                break
            roto, cont = ataque_combinaciones(
                config["temppassphrase"],
                partes, trabajo[0], trabajo[1])
            if roto:
                servicio.servir_avisar_roto(cont)
            else:
                servicio.servir_avisar_final(trabajo)

def administrar_ataque_combinacion(fichpassph, fuente, conti):
    global cantpp
    roto = False
    cont = []
    partes = lee_partes(fuente)
    elimina_repeticiones(partes)
    base = len(partes)
    contfsel = conti
    while not roto:
        # Selecciona el próximo paquete.
        contisel = contfsel.copy()
        sumarle_decimal_contador(contfsel, base, cantpp)
        # Prueba todas las combinaciones del paquete.
        roto, cont = ataque_combinaciones(fichpassph, partes, contisel, contfsel)

def armar_combinacion(partes, contador):
    combinacion = ""
    for i in contador:
        combinacion += partes[i]
    return combinacion

def ataque_combinaciones(fichpassph, partes, conti, contf):
    global inicio
    print("Haciendo el ataque de combinaciones de partes de cadenas")
    print("Probando del {} al {}.".format(conti, contf))
    # print("ataque_combinaciones {} {} {}".format(partes, conti, contf))
    roto = False
    combinacion = ""
    cprob = 0
    base = len(partes)
    print("Probando combinaciones con {} partes.".format(base))
    while verificar_menor(conti, contf):
        # print(conti)
        combinacion = armar_combinacion(partes, conti)
        # Prueba la combinación.
        roto = probarPalabra(fichpassph, combinacion)
        cprob += 1
        # Imprime el punto o el reporte si toca hacerlo.
        if (cprob % cantcp) == 0:
            print(".", end = "", flush = True)
        if (cprob % cantpr) == 0:
            actual = datetime.datetime.now()
            print("\nCantidad: {} Contador: {} Combinacion: \"{}\" Tiempo: {}".format(
                cprob, conti, combinacion, actual - inicio))
            print("Probando {} combinaciones por minuto".format(
                math.floor(cprob / ((actual - inicio).total_seconds() / 60)) ))
        # Si encontraste la combinación rompe el bucle.
        if roto:
            print("Encontré el passphrase, es la palabra \"{}\"!!".format(combinacion))
            break
        # Aumenta el contador.
        sumarle_decimal_contador(conti, base, 1)
    print("Probé {} combinaciones.".format(cprob))
    return (roto, conti)

def main():
    global inicio, final
    contadores = [0]
    # Revisa los argumentos.
    if ((len(sys.argv) < 3)
        or ((sys.argv[1].lower().strip() == "--servidor")
            and (len(sys.argv) < 4) )):
        print("El uso correcto es: \n    \"romper-ecryptfs.py --servidor "
              + " /home/pedro/.ecryptfs/wrapped-passphrase "
              + "/home/pedro/diccionario.txt\" \n    o\n    \""
              + "romper-ecryptfs.py --cliente http://servidor/\"")
        sys.exit(1)
    # Toma el tiempo de inicio.
    inicio = datetime.datetime.now()
    print("Comenzando a las {}".format(inicio))
    if sys.argv[1].strip().lower() == "--servidor":
        for arg in sys.argv[4:]:
            if arg.startswith("--cont="):
                contadores = [int(parte) for parte in arg[len("--cont="):].split("-")]
                print("Iniciando en Contador {}".format(contadores))
        print("Tratando de romper el passpharse {}.".format(sys.argv[2]))
        administrar_servidor(sys.argv[2], sys.argv[3], contadores)
    elif sys.argv[1].strip().lower() == "--cliente":
        administrar_cliente(sys.argv[2])
    # Toma el tiempo final
    final = datetime.datetime.now()
    # Haz un reporte final del tiempo
    print("Comenzamos a hacer intentos en: {}".format(inicio))
    print("Terminamos en: {}".format(final))
    print("Tomó: {}".format(final - inicio))

if __name__ == "__main__":
    main()
