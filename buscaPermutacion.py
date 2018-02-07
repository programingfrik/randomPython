#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Este es un programita para resolver el problema de mi amiga Lucia de
# adivinar a que animal se refiere cada una de las siguientes
# permutaciones de caracteres:
#
# 1 - fabulo
# 2 - locabal
# 3 - localme
# 4 - vicero
# 5 - irmoderado
# 6 - anteelfe
# 7 - toga
# 8 - elon
# 9 - dorapelo
# 10 - comas
# 11 - trapean
# 12 - grite
#


import sys
import urllib.request

def permutar(palabra, estado):
    # incrementa el estado
    lleva = 0
    c = len(estado) - 1
    estado[c] += 1    
    while c >= 0:
        estado[c] += lleva
        lleva = 0
        maximo = len(estado) - c
        if estado[c] > maximo:
            estado[c] = 0
            lleva = 1
        c -= 1
    # arma la permutación que le corresponde a ese estado.
    palabra = list(palabra)
    combinacion = []
    c = 0
    while c < len(estado):
        combinacion.append(palabra.pop(estado[c]))
        c += 1
    combinacion.append(palabra[0])
    # devuelve la combinación y su estado.
    return "".join(combinacion), estado, lleva

def probarPermutacion(palabra, fuentes):
    # print("buscando \"{}\"".format(palabra))
    for fuente in fuentes:
        direccion = fuente + palabra
        # si encuentra la permutación en esta fuente, entonces esta es la palabra.
        try:
            request = urllib.request.urlopen(direccion)
            codigo = request.getcode()
        except:
            codigo = 404
        finally:
            if 'request' in locals():
                request.close()
        if codigo == 200:
            print("Encontré \"{}\" en \"{}\".".format(palabra, direccion))
            return True
    return False

fuentes = ["https://es.wikipedia.org/wiki/",
           "https://es.wiktionary.org/wiki/"]

# tomar el argumento
palabra = sys.argv[1]
estado = [0] * (len(palabra) - 1)
combinacion = palabra
lleva = 0
encontrada = False
while lleva == 0:
    # prueba cada permutación de la palabra que se pasó como parámetro
    print("La palabra que vamos a probar es \"{}\".".format(combinacion))
    # verifica la permutación
    encontrada = probarPermutacion(combinacion, fuentes)
    if encontrada:
        print("\n\nLa palabra correcta es {}\n".format(combinacion))
        break
    combinacion, estado, lleva = permutar(palabra, estado)

if not encontrada:
    print("La palabra no fue encontrada.")
    
print("Listo!")
