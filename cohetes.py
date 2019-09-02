#!/usr/bin/python3

#
# Esto es un script para elaborar frases cohetes usando los
# maravillosos conocimientos obtenidos de esta página:
#
#   http://paginaspersonales.deusto.es/airibar/Personal/Textos_web/Textos_lenguaje.html
#

import random
import sys
import re

ffrases = "cohete1.txt"
fdiscurso = "cohete2.txt"
titulo = re.compile("^\\[\\w+\\]$")

def cargarColumnas(fichero):
    global titulo
    columnas = []
    temp = []
    with open(fichero, "r", errors="replace") as f:
        linea = f.readline()
        while linea != "":
            linea = linea.replace("\n", "").strip()
            if titulo.match(linea):
                if len(temp) > 0:
                    columnas.append(temp)
                    temp = []
            elif linea != "":
                temp.append(linea)
            linea = f.readline()
        if len(temp) > 0:
            columnas.append(temp)
    return columnas

def armarFrase(columnas):
    frase = ""
    for columna in columnas:
        if len(columna) > 0:
            frase += " " + random.choice(columna)
    return frase

def generarFrase():
    global ffrases
    columnas = cargarColumnas(ffrases)
    frase = armarFrase(columnas)
    print(frase)

def generarDiscurso(cant):
    global fdiscurso
    discurso = ""
    columnas = cargarColumnas(fdiscurso)
    for i in range(cant):
        discurso += " " + armarFrase(columnas)
    print(discurso)

def main():
    if ((len(sys.argv) == 2)
        and (sys.argv[1].upper() == "FRASE")):
        generarFrase()
    elif ((len(sys.argv) == 3)
          and (sys.argv[1].upper() == "DISCURSO")
          and (sys.argv[2].isdigit())):
        generarDiscurso(int(sys.argv[2]))
    else:
        print("Error parámetros equivocados!\n\nLo correcto "
              + "es:\n cohetes.py frase\n cohetes.py discurso N")

if __name__ == "__main__":
    main()
