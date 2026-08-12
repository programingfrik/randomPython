#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto es un script para crear y probar una función python que calcule
# las coordenadas de una recta normal a una recta descrita por los
# puntos A y B, a una distancia H.

import math

def rotar_punto(p, a):
    prx = p[0] * math.cos(a) - p[1] * math.sin(a)
    pry = p[0] * math.sin(a) + p[1] * math.cos(a)
    return prx, pry

def calcular_perpendicular(a, b, h):
    X = 0
    Y = 1

    med = ((b[X] + a[X]) // 2, (b[Y] + a[Y]) // 2)

    # Calculando la pendiente
    if b[X] != a[X]:
        m = (b[Y] - a[Y]) // (b[X] - a[X])
    elif b[Y] > a[Y]:
        m = 0; # + infinito
    elif b[Y] < a[Y]:
        m = 0; # - infinito

    vr = b[X] - a[X], b[Y] - a[Y]

    avr = math.atan2(vr[Y], vr[X])

    return med

def probar_calculo(a, b, h, c, mensaje = None):
    if mensaje:
        mensaje += " "
    else:
        mensaje = "prueba "

    print(f"Haciendo {mensaje}calcular_perpendicular"
          + f"({a}, {b}, {h})\n    Esperado {c}")

    cc = calcular_perpendicular(a, b, h)

    print(f"    Valor obtenido {cc}\n    ", end = "")

    if (c != cc):
        print("No ", end = "")

    print("Pasó!\n")

def main():
    probar_calculo((5, 0), (15, 0), 5, (10, 5), "prueba evidente 1")
    probar_calculo((15, 0), (5, 0), 5, (10, -5), "prueba evidente 2")
    probar_calculo((5, 5), (5, 15), 5, (0, 10), "prueba evidente 3")

if __name__ == "__main__":
    main()

