#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esto un programa para simular lo que se
# ve en las pantallas de las computadoras en
# la película "Matrix" que creo esta basado
# en algo que pasa con los créditos en la
# pélicula "Ghost in the Shell". Este es
# un programa que aprendí a hacer en Turbo
# Basic con un amigo de ITESA que se llama
# Emmanuel Abreu (satanclos) ...

# The Matrix by Pablo Mercader Alcántara

import curses
import time
import math
import random
import sys

# inicializando
maxY, maxX = 0, 0
maxE = 20

# caracteres que no se deberían usar porque estan en blanco o son caracteres de control.
excepciones = [0, 3]

class claseColumna:
    def __init__(self):
        self.reset()

    def reset(self):
        global maxY, maxX, maxE
        self.col = random.randrange(maxX)
        self.ya = 0
        self.yf = random.randrange(maxY)
        self.tono = random.randrange(1, 5)
        self.espera = random.randrange(1, maxE)

def seleccionarCar():
    return chr(random.randrange(32, 255))

def escenaTitulo(stdscr):
    global maxY, maxX
    texto = "The Matrix"
    x = math.floor((maxX - len(texto))/ 2)
    y = math.floor(maxY / 2)

    secuencia = [4, 3, 2, 1, 2, 3]

    for color in secuencia:
        stdscr.addstr(y, x, texto, curses.color_pair(color))
        if (color == 1):
            curses.flash()        
        stdscr.refresh()
        time.sleep(0.1)

def escenaTexto(stdscr):
    global maxY, maxX
    totalCar = 255
    ccol = 10
    columnas = []
    
    for i in range(ccol):
        columnas += [claseColumna()]

    while (True):
        for col in columnas:
            if col.ya < col.yf:
                car = seleccionarCar()
                stdscr.addstr(col.ya, col.col, car,
                              curses.color_pair(col.tono))
                stdscr.refresh()
                time.sleep(0.005)
                col.ya += 1
            elif col.espera > 0:
                col.espera -= 1
            else:
                col.reset()
            
        if (stdscr.getch() != curses.ERR):
            break
                
def matrixMain(stdscr):
    global maxY, maxX
    # el cuerpo
    
    # por alguna razón desconocida no puedo desaparecer el cursor en windows (cygwin)
    if ("linux" in sys.platform):
        curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
    stdscr.leaveok(1)
    stdscr.nodelay(1)
    maxY, maxX = stdscr.getmaxyx()

    escenaTitulo(stdscr)

    escenaTexto(stdscr)

# la función wrapper hace las inicializaciones y finalizaciones necesarias.
curses.wrapper(matrixMain)
