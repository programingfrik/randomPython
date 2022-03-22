#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto es un script para tratar de romper un passphrase de ecryptfs usando fuerza bruta.

import sys
import pexpect
import datetime
import math
import xmlrpc.server
import xmlrpc.client
import csv
from pathlib import Path

config = {
    "ecryptcomm": "ecryptfs-unwrap-passphrase",
    "temppassphrase": "/tmp/wrapped-passphrase-temp"
}

inicio = None
final = None
cantcp = 10   # Cantidad de combinaciones probadas por punto.
cantpr = 100  # Cantidad de pruebas por reporte.
cprob = 0   # Cantidad de combinaciones probadas hasta el momento.


cantpp = 1000 # Cantidad de pruebas por paquete.
maxtp = datetime.timedelta(seconds = 60 * 10) # El tiempo máximo que se va a esperar un paquete.

partes = []   # La lista de las partes.
contfichpassph = None # El contenido del ficher passphrase.
roto = False  # Indica si ya logramos romper el passphrase.

conti = [0]   # El contador inicial.

pizarron = [] # El pizarrón para llevar el estado de los trabajos.
fichpizarron = "" # El fichero donde está guardado el pizarron.
mintep = datetime.timedelta(seconds = 60 * 5) # El tiempo mínimo de escritura del pizarron, el tiempo mínimo que tiene que esperar para volver a escribir el pizarron al fichero.
momue = None # Momento de la última escritura.

puerto = 8080 # El puerto del servidor por el que se va a producir la comunicación.

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
    if n > len(contador):
        temp = ([0] * (n - len(contador))) + contador
        return temp
    else:
        return contador

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
    tpaquete = []
    print("Sirviendo trabajo ...")
    # Verifica si ya fue roto el passphrase, si lo fue no hay que
    # seguir dando trabajos.
    if roto:
        tpaquete = []
    # Verifica el pizarrón
    elif (pizarron == None) or (len(pizarron) == 0):
        # Si el pizarrón está vacío registra el primer trabajo.
        print("El pizarron no existe, creando el primer trabajo ...")
        contisel = conti
        contfsel = conti.copy()
        sumarle_decimal_contador(contfsel, base, cantpp)
        tpaquete = [contisel, contfsel, datetime.datetime.now(), 1]
        pizarron.append(tpaquete)
    else:
        # Sino, si el pizarrón ya existe, ya tiene trabajos,
        # verificalo en busca de trabajos.
        for paquete in pizarron:
            # print("Comparando {}".format(paquete))
            if (paquete[3] == 1) and ((datetime.datetime.now() - paquete[2]) > maxtp):
                # Si encuentras un trabajo que ya se le pasó el tiempo, tomalo.
                print ("Sirviendo trabajo viejo ...")
                paquete[2] = datetime.datetime.now()
                tpaquete = paquete
                break
            elif (contfante != None) and (restar_contador(paquete[0], contfante) > 0):
                # Sino, si encuentras un espacio entre 2 trabajos, tomalo.
                print ("Armando un trabajo entre 2 trabajos previos ...")
                contisel = contfante
                contfsel = contfante.copy()
                tam_esp = restar_contador(paquete[0], contfante)
                if tam_esp >= cantpp:
                    tam_esp = cantpp
                sumarle_decimal_contador(contfsel, base, tam_esp)
                tpaquete = [contisel, contfsel, datetime.datetime.now(), 1]
                break
        else:
            # Sino, agrega uno nuevo al final.
            print("Sirviendo un trabajo nuevo ...")
            contisel = pizarron[-1][1]
            contfsel = pizarron[-1][1].copy()
            sumarle_decimal_contador(contfsel, base, cantpp)
            tpaquete = [contisel, contfsel, datetime.datetime.now(), 1]
        pizarron.append(tpaquete)
    escribir_pizarron()
    print("Sirviendo {}.".format(tpaquete))
    return tpaquete

def verificar_continuos(paqueteA, paqueteB):
    return (((paqueteA[3] == 0) and (paqueteA[3] == paqueteB[3]))
            and ((paqueteA[1] == paqueteB[0]) or (paqueteB[1] == paqueteA[0])))

def verificar_solapados(paqueteA, paqueteB):
    tam = max([len(paqueteA[0]), len(paqueteA[1]),
               len(paqueteB[0]), len(paqueteB[1])])
    tempA1 = completa_ceros(paqueteA[0], tam)
    tempA2 = completa_ceros(paqueteA[1], tam)
    tempB1 = completa_ceros(paqueteB[0], tam)
    tempB2 = completa_ceros(paqueteB[1], tam)
    return (((paqueteA[3] == 0) and (paqueteA[3] == paqueteB[3]))
            and (((tempA1 <= tempB1) and (tempB1 < tempA2))
                 or ((tempA1 <= tempB2) and (tempB2 < tempA2))))

def mezclar_paquetes(paqueteA, paqueteB):
    tam = max([len(paqueteA[0]), len(paqueteA[1]),
               len(paqueteB[0]), len(paqueteB[1])])
    tempA1 = completa_ceros(paqueteA[0], tam)
    tempA2 = completa_ceros(paqueteA[1], tam)
    tempB1 = completa_ceros(paqueteB[0], tam)
    tempB2 = completa_ceros(paqueteB[1], tam)
    if tempA1 <= tempB1:
        conti = paqueteA[0]
    else:
        conti = paqueteB[0]
    if tempA2 > tempB2:
        contf = paqueteA[1]
    else:
        contf = paqueteB[1]
    if paqueteA[2] < paqueteB[2]:
        momento = paqueteA[2]
    else:
        momento = paqueteB[2]
    return [conti, contf, momento, 0]

def servir_avisar_final(paquete):
    global pizarron
    i = 0
    print("Recibiendo aviso de final ...")
    # Recorre los trabajos en el pizarrón
    # print("Paquete {}".format(paquete))
    # print("Pizarrón {}".format(pizarron))
    while i < len(pizarron):
        # Si aparece el trabajo que acaba de terminar ponlo en 0
        # print("Comparando {} con {}".format(paquete[0], pizarron[i][0]))
        if paquete[0] == pizarron[i][0]:
            pizarron[i][3] = 0
        # Si hay un trabajo previo al actual en el pizarron, también
        # terminado, y son continuos o se solapan, concatenalos en uno
        # solo para evitar tener un montón de intervalos sueltos.
        if ((i > 0) and (verificar_continuos(pizarron[i - 1], pizarron[i])
                         or verificar_solapados(pizarron[i - 1], pizarron[i]))):
            pizarron[i - 1] = mezclar_paquetes(pizarron[i - 1], pizarron[i])
            del(pizarron[i])
        else:
            i += 1
    escribir_pizarron()
    return 0

def servir_avisar_roto(contador):
    global roto, partes
    roto = True
    print("Recibiendo aviso de passphrase roto ...")
    combinacion = armar_combinacion(partes, contador)
    print("Encontré el passphrase, es la palabra \"{}\", la combinacion {}."
          .format(combinacion, contador))
    return 0

def administrar_servidor(fichpassph, fuente, conti):
    global pizarron, partes, contfichpassph, cantpp, roto, puerto
    print("Iniciando servidor en el puerto {}.".format(puerto))
    partes = lee_partes(fuente)
    elimina_repeticiones(partes)
    contfichpassph = lee_fichpassph(fichpassph)
    with xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", puerto)) as servidor:
        servidor.register_introspection_functions()
        servidor.register_function(servir_partes)
        servidor.register_function(servir_fichpassph)
        servidor.register_function(servir_trabajo)
        servidor.register_function(servir_avisar_final)
        servidor.register_function(servir_avisar_roto)
        try:
            servidor.serve_forever()
        except (KeyboardInterrupt, Exception) as exp:
            escribir_pizarron(ver_mintep = False)
            raise exp

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
            if len(trabajo) == 0:
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
    global inicio, cprob
    print("Haciendo el ataque de combinaciones de partes de cadenas")
    print("Probando del {} al {}.".format(conti, contf))
    # print("ataque_combinaciones {} {} {}".format(partes, conti, contf))
    cont = conti.copy()
    roto = False
    combinacion = ""
    base = len(partes)
    print("Probando combinaciones con {} partes.".format(base))
    while completa_ceros(cont, len(contf)) < completa_ceros(contf, len(cont)):
        # print(cont)
        combinacion = armar_combinacion(partes, cont)
        # Prueba la combinación.
        roto = probarPalabra(fichpassph, combinacion)
        cprob += 1
        # Imprime el punto o el reporte si toca hacerlo.
        if (cprob % cantcp) == 0:
            print(".", end = "", flush = True)
        if (cprob % cantpr) == 0:
            actual = datetime.datetime.now()
            print("\nCantidad: {} Contador: {} Combinacion: \"{}\" Tiempo: {}".format(
                cprob, cont, combinacion, actual - inicio))
            print("Probando {} combinaciones por minuto".format(
                math.floor(cprob / ((actual - inicio).total_seconds() / 60)) ))
        # Si encontraste la combinación rompe el bucle.
        if roto:
            print("Encontré el passphrase, es la palabra \"{}\"!!".format(combinacion))
            break
        # Aumenta el contador.
        sumarle_decimal_contador(cont, base, 1)
    print("Probé {} combinaciones.".format(cprob))
    return (roto, cont)

def escribir_pizarron(ver_mintep = True):
    global fichpizarron, pizarron, mintep, momue
    if (((ver_mintep) and (momue != None)
        and ((datetime.datetime.now() - momue) < mintep))
        or (fichpizarron == "")):
        return
    print("Escribiendo fichero pizarron \"{}\"".format(fichpizarron))
    momue = datetime.datetime.now()
    with open(Path(fichpizarron).expanduser(), "w", newline="") as hfpizarron:
        escritorcsv = csv.writer(hfpizarron, delimiter = ",", quotechar="\"")
        for paquete in pizarron:
            conti = "-".join([str(v) for v in paquete[0]])
            contf = "-".join([str(v) for v in paquete[1]])
            escritorcsv.writerow([conti, contf, paquete[2].isoformat(), paquete[3]])

def lee_pizarron():
    global fichpizarron, pizarron
    conti = []
    contf = []
    pizarron = []
    if not Path(Path(fichpizarron).expanduser()).exists():
        return
    print ("Tratando de leer el fichero \"{}\".".format(fichpizarron))
    with open(Path(fichpizarron).expanduser(), "r", newline = "") as hfpizarron:
        lectorcsv = csv.reader(hfpizarron, delimiter = ",", quotechar="\"")
        for fila in lectorcsv:
            conti = [int(v) for v in fila[0].split("-")]
            contf = [int(v) for v in fila[1].split("-")]
            pizarron.append([conti, contf, datetime.datetime
                             .fromisoformat(fila[2]), int(fila[3])])
    print("Leido el pizarron {}.".format(pizarron))

def main():
    global inicio, final, fichpizarron
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
            elif arg.startswith("--pizarron="):
                fichpizarron = arg[len("--pizarron="):]
                lee_pizarron()
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
