#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto es un script para crear y probar una función python que calcule
# las coordenadas de una recta normal a una recta descrita por los
# puntos A y B, a una distancia H.

import math

X = 0
Y = 1

def rotar_punto(p, a):
    global X, Y
    prx = p[X] * math.cos(a) - p[Y] * math.sin(a)
    pry = p[X] * math.sin(a) + p[Y] * math.cos(a)
    return prx, pry

def normalizar(v):
    global X, Y
    modulo = math.sqrt(v[X] ** 2 + v[Y] ** 2)
    vn = v[X] / modulo, v[Y] / modulo
    return vn

def calcular_perpendicular(a, b, h):
    global X, Y

    # Calcula el punto medio
    med = ((b[X] + a[X]) / 2, (b[Y] + a[Y]) / 2)

    # Calcula el "vertor real"
    vr = b[X] - a[X], b[Y] - a[Y]

    # Normaliza el vector real
    vrn = normalizar(vr)

    # Rota 90 grados, o pi / 2, el vector real normalizado
    vrnr = rotar_punto(vrn, math.pi / 2)

    # Solo queda multiplicarlo por h para que tenga la longitud
    # solicitada y trasladarlo al sitio del punto medio.
    vp = (vrnr[X] * h) + med[X], (vrnr[Y] * h) + med[Y]

    return vp

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
    probar_calculo((5, 5), (15, 15), 5, (15, 5), "prueba evidente diagonal 45 grados")

if __name__ == "__main__":
    main()

