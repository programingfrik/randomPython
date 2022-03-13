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
cantpp = 10   # Cantidad de pruebas por punto.
cantpr = 1000  # Cantidad de pruebas por reporte.

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

def elimina_duplicados(partes):
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

def ataque_combinaciones(fichpassph, fuente, contadores):
    global inicio
    print("Haciendo el ataque de combinaciones de strings")
    combinacion = ""
    roto = False
    cprob = 0
    partes = lee_partes(fuente)
    # Elimina todas las repeticiones
    elimina_duplicados(partes)
    cant = len(partes)
    print("Probando combinaciones con {} cadenas.".format(cant))
    while not roto:
        # print(contadores)
        combinacion = ""
        # Arma la combinación.
        for i in contadores:
            combinacion += partes[i]
        # Prueba la combinación.
        roto = probarPalabra(fichpassph, combinacion)
        cprob += 1
        if (cprob % cantpp) == 0:
            print(".", end = "", flush = True)
        if (cprob % cantpr) == 0:
            actual = datetime.datetime.now()
            print("\nCantidad: {} Contador: {} Combinacion: \"{}\" Tiempo: {}".format(
                cprob, contadores, combinacion, actual - inicio))
            print("Probando {} combinaciones por minuto".format(
                math.floor(cprob / ((actual - inicio).total_seconds() / 60)) ))
        # Si encontraste la combinación rompe el bucle.
        if roto:
            print("Encontré le passphrase la palabra \"{}\"!!".format(combinacion))
            break
        # Aumenta los contadores.
        i = 0
        # Aumenta el contador 0
        contadores[i] += 1
        # Mientras sea necesario propagar a los siguientes contadores recorrelos.
        while contadores[i] >= len(partes):
            contadores[i] = 0
            if i == (len(contadores) - 1):
                contadores.append(0)
            else:
                i += 1
                contadores[i] += 1
    print("Probé {} combinaciones.".format(cprob))

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
    # toma el tiempo de inicio
    inicio = datetime.datetime.now()
    print("Comenzando a las {}".format(inicio))
    ataque_combinaciones(sys.argv[1], sys.argv[2], contadores)
    # toma el tiempo final
    final = datetime.datetime.now()
    # Haz un reporte final del tiempo
    print("Comenzamos a hacer intentos en: {}".format(inicio))
    print("Terminamos en: {}".format(final))
    print("Tomó: {}".format(final - inicio))

if __name__ == "__main__":
    main()
