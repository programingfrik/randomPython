#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Imitando el buscaminas de windows, esto es un tributo al juego ese
# en el que perdimos tanto tiempo, pero hecho en python3/tkinter

# La idea de hacer esto surgió en casa de Julio, pc nueva, sin juegos,
# un tonto propuso "hagamos el buscaminas en python", y bueno no se
# hizo en el momento pero ahora si.

# Este código se lo dedico a mi enemigo pelsonal Fernando Franco y a
# mi amigo el español nacido en RD Julio Thomas Gutierrez Lora.

from tkinter import *
from tkinter.messagebox import *
from tkinter.font import *
import random
import datetime

class BuscaMinas(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.cantx = 10
        self.canty = 10
        self.cantm = 10
        self.minas = []
        self.posibles = 0
        self.bloqueado = False
        self.encurso = False
        self.tinicio = None
        self.cantp = 0
        self.fondoNormal = ""
        self.ponerMinas()
        self.crearControles(master)

    def crearControles(self, master):
        top = Frame(master)
        top.grid(sticky = N + S + E + W)
        # configura la letra que van a usar los controles
        fontNormal = Font(size = 12, weight = "bold")
        # configura el cronomentro
        self.tiempo = StringVar()
        self.tiempo.set("00:00")
        self.lbTiempo = Label(top, textvariable = self.tiempo,
                              font = fontNormal)
        self.lbTiempo.grid(row = 0, column = 0)
        self.configurarDisplay(self.lbTiempo)
        # configura la carita el botón de reiniciar
        self.carita = StringVar()
        self.carita.set(":-)")
        self.btCarita = Button(top, textvariable = self.carita,
                               font = fontNormal)
        self.btCarita.bind("<Button-1>", self.reiniciar)
        self.btCarita.bind("<ButtonRelease-1>", self.reiniciar)
        self.btCarita.grid(row = 0, column = 1)
        self.fondoNormal = self.btCarita.cget("background")
        self.configurarCarita(self.btCarita)
        # configura el contador de minas
        self.cantMAct = StringVar()
        self.actualizarCantM()
        self.lbMinas = Label(top, textvariable = self.cantMAct,
                             font = fontNormal)
        self.lbMinas.grid(row = 0, column = 2)
        self.configurarDisplay(self.lbMinas)
        # configura 'to los botone eso de la cuadricula
        self.fBotones = Frame(top)
        self.fBotones.grid(row = 1, column = 0, columnspan = 3)
        self.botones = []
        for i in range(self.cantx):
            temp = []
            for j in range(self.canty):
                txTemp = StringVar()
                btTemp = Button(self.fBotones, width = 1,
                                textvariable = txTemp, font = fontNormal)
                btTemp.idx = i
                btTemp.idy = j
                btTemp.bind("<ButtonRelease-1>", self.pisada)
                btTemp.bind("<ButtonRelease-3>", self.pisada)
                btTemp.grid(row = i, column = j)
                self.configurarBoton(btTemp, "", txTemp)
                temp.append((btTemp, txTemp))
            self.botones.append(temp)
            
    def actualizarCantM(self):
        self.cantMAct.set(str(self.cantm - self.posibles))
    
    def reiniciar(self, event):
        if event.type == "4":
            self.carita.set(":-o")
        elif event.type == "5":
            self.carita.set(":-)")
        self.ponerMinas()
        self.limpiarBotones()
        self.posibles = 0
        self.bloqueado = False
        self.encurso = False
        self.tiempo.set("00:00")
        self.actualizarCantM()
        self.cantp = 0

    def pisada(self, event):
        # print ("{}, {}".format(self.cantp, ((self.cantx * self.canty) - self.cantm)))
        if self.bloqueado:
            return
        if self.encurso == False:
            self.encurso = True
            self.iniciarReloj()
        idx = event.widget.idx
        idy = event.widget.idy
        valor = self.valorBoton(idx, idy)
        if (event.num == 1) and (valor == ""):
            if (idx, idy) in self.minas:
                self.mostrarMinas()
                self.carita.set(":-(")
                self.bloqueado = True
                self.encurso = False
                valor = "@"
            else:
                # print("contando {},{}".format(idx, idy))
                self.cantp += 1
                valor = str(self.contarMinas(idx, idy))
            self.configurarBoton((idx, idy), valor)
            if valor == "0":
                self.carita.set(":-o")
                # print("{}, {} es 0!!".format(idx, idy))
                self.mostrarCeros(idx,idy)
                self.carita.set(":-)")
            if self.cantp == ((self.cantx * self.canty) - self.cantm):
                self.encurso = False
                self.bloqueado = True
                self.carita.set("8-D")
                showinfo("Busca Minas", "Lo has logrado tío! Contratulaciones!")
        elif event.num == 3:
            if valor == "X":
                valor = ""
                self.posibles -= 1
            elif valor == "":
                valor = "X"
                self.posibles += 1
            self.actualizarCantM()
            self.configurarBoton((idx, idy), valor)

    def ponerMinas(self):
        self.minas = []
        random.seed()
        for i in range(self.cantm):
            mx = random.randint(0, self.cantx - 1)
            my = random.randint(0, self.canty - 1)
            self.minas.append((mx, my))

    def mostrarMinas(self):
        for mina in self.minas:
            x = mina[0]
            y = mina[1]
            valor = self.valorBoton(x, y)
            if valor == "X":
                valor = "#"
            else:
                valor = "*"
            self.configurarBoton((x, y), valor)

    def contarMinas(self, x, y):
        vecinos = [(x - 1, y - 1),
                   (x - 1, y),
                   (x - 1, y + 1),
                   (x, y - 1),
                   (x, y + 1),
                   (x + 1, y - 1),
                   (x + 1, y),
                   (x + 1, y + 1)]
        cont = 0
        for vecino in vecinos:
            if vecino in self.minas:
                cont += 1
        return cont

    def limpiarBotones(self):
        for i in range(self.cantx):
            for j in range(self.canty):
                self.configurarBoton((i, j), "")

    def mostrarCeros(self, x, y):
        # print("mostrando ceros para {}, {}".format(x, y))
        vecinos = [(x - 1, y),
                   (x, y - 1),
                   (x, y + 1),
                   (x + 1, y)]
        for vecino in vecinos:
            vx = vecino[0]
            vy = vecino[1]
            if (((vx >= 0) and (vx < self.cantx))
                and ((vy >= 0) and (vy < self.canty))
                and (self.valorBoton(vx, vy) == "")):
                self.cantp += 1
                # print("contando {}, {}".format(vx, vy))
                cont = self.contarMinas(vx, vy)
                if cont == 0:
                    # print("{}, {} es 0!!".format(vx, vy))
                    # input()
                    self.configurarBoton((vx, vy), str(cont))
                    self.mostrarCeros(vx, vy)
                else:
                    self.configurarBoton((vx, vy), str(cont))
                    
    def iniciarReloj(self):
        self.tinicio = datetime.datetime.now()
        self.actualizarReloj()
    
    def actualizarReloj(self):
        tactual = datetime.datetime.now() - self.tinicio
        self.tiempo.set("{:02}:{:02}".format(
            tactual.seconds // 60, tactual.seconds % 60))
        if self.encurso:
            self.after(500, self.actualizarReloj)

    def configurarDisplay(self, control):
        control.configure(foreground = "#f00", background = "#500")

    def configurarCarita(self, control):
        control.configure(background = "yellow",
                          activebackground = "yellow")

    def valorBoton(self, x, y):
        return self.botones[x][y][1].get()

    def configurarBoton(self, control, texto, vartexto=None):
        if type(control) is tuple:
            # print("{}, {}".format(texto, type(texto)))
            self.botones[control[0]][control[1]][1].set(texto)
            control = self.botones[control[0]][control[1]][0]
        else:
            vartexto.set(texto)
        colores = {"": (None, None),
                   "0": ("#AAAAAA", None),
                   "1": ("#00FF00", None),
                   "2": ("#55FF00", None),
                   "3": ("#AAFF00", None),
                   "4": ("#FFFF00", None),
                   "5": ("#FFAA00", None),
                   "6": ("#FF5500", None),
                   "7": ("#FF0000", None),
                   "8": ("#FF0000", None),
                   "X": ("#000000", None),
                   "*": ("#000000", None),
                   "@": ("#000000", "#FF0000"),
                   "#": ("#000000", None)}
        poner = {}
        if colores[texto][0]:
            poner["foreground"] = colores[texto][0]
        if colores[texto][1]:
            poner["background"] = colores[texto][1]
        else:
            poner["background"] = self.fondoNormal
        if poner:
            control.configure(**poner)
        
app = BuscaMinas()
app.master.title("Busca Minas")
app.mainloop()
