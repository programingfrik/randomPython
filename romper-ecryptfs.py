#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto es un script para tratar de romper un passphrase de ecryptfs usando fuerza bruta.

import sys
import pexpect
import datetime
import math

config = {
    "ecryptcomm": "ecryptfs-unwrap-passphrase"
}
inicio = None
final = None
cantcp = 10   # Cantidad de combinaciones probadas por punto.
cantpr = 100  # Cantidad de pruebas por reporte.
cantpp = 1000 # Cantidad de pruebas por paquete.

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

def administrar_ataque_combinacion(fichpassph, fuente, conti):
    global cantpp
    roto = False
    partes = lee_partes(fuente)
    elimina_repeticiones(partes)
    base = len(partes)
    contfsel = conti
    while not roto:
        # Selecciona el próximo paquete.
        contisel = contfsel.copy()
        sumarle_decimal_contador(contfsel, base, cantpp)
        # Prueba todas las combinaciones del paquete.
        roto = ataque_combinaciones(fichpassph, partes, contisel, contfsel)

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
        combinacion = ""
        # Arma la combinación.
        for i in conti:
            combinacion += partes[i]
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
    return roto

def main():
    global inicio, final
    contadores = [0]
    # Revisa los argumentos.
    if len(sys.argv) < 3:
        print("El uso correcto es \"romper-ecryptfs.py"
              + " /home/pedro/.ecryptfs/wrapped-passphrase\""
              + " /home/pedro/diccionario.txt")
        sys.exit(1)
    for arg in sys.argv[3:]:
        if arg.startswith("--cont="):
            contadores = [int(parte) for parte in arg[len("--cont="):].split("-")]
            print("Iniciando en Contador {}".format(contadores))
    print("Tratando de romper el passpharse {}.".format(sys.argv[1]))
    # Toma el tiempo de inicio.
    inicio = datetime.datetime.now()
    print("Comenzando a las {}".format(inicio))
    administrar_ataque_combinacion(sys.argv[1], sys.argv[2], contadores)
    # Toma el tiempo final
    final = datetime.datetime.now()
    # Haz un reporte final del tiempo
    print("Comenzamos a hacer intentos en: {}".format(inicio))
    print("Terminamos en: {}".format(final))
    print("Tomó: {}".format(final - inicio))

if __name__ == "__main__":
    main()
