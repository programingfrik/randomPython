#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto es un script para tratar de romper un passphrase de ecryptfs usando fuerza bruta.

import sys
import pexpect

config = {
    "ecryptcomm": "ecryptfs-unwrap-passphrase"
}

def probarPalabra(fichpassph, palabra):
    global config
    print("Probando \"{}\"".format(palabra))
    expdor = pexpect.spawn("{0} {1}" .format(config["ecryptcomm"], fichpassph))
    expdor.expect("Passphrase: ")
    expdor.sendline(palabra)
    resp = expdor.expect(["Error: ", "[a-z0-9]{10,}"])
    if resp == 0:
        print("Falló la palabra \"{}\"".format(palabra))
        return False
    else:
        print("La clave \"{}\" fue exitosa.".format(palabra))
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

def ataque_combinaciones(fichpassph, fuente):
    print("Haciendo el ataque de combinaciones de strings")
    partes = []
    contadores = [0]
    combinacion = ""
    roto = False
    with open(fuente, "r") as hfuente:
        # Pon todas las lineas de fuente en partes.
        for linea in hfuente:
            valor = linea[:-1].strip()
            partes.append(valor)
    cant = len(partes)
    while not roto:
        combinacion = ""
        # Arma la combinación.
        for i in contadores:
            combinacion += partes[i]
        # Prueba la combinación.
        roto = probarPalabra(fichpassph, combinacion)
        # Si encontraste la combinación rompe el bucle.
        if roto:
            print("Encontré le passphrase la palabra \"{}\"!!".format(palabra))
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

def main():
    # Revisa los argumentos.
    if len(sys.argv) != 3:
        print("El uso correcto es \"romper-ecryptfs.py"
              + " /home/pedro/.ecryptfs/wrapped-passphrase\""
              + " /home/pedro/diccionario.txt")
        sys.exit(1)
    print("Tratando de romper el passpharse {}.".format(sys.argv[1]))
    ataque_combinaciones(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
