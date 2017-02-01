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
        self.ponerMinas()
        self.crearControles(master)

    def crearControles(self, master):
        top = Frame(master)
        top.grid(sticky = N + S + E + W)
        self.tiempo = StringVar()
        self.tiempo.set("00:00")
        self.lbTiempo = Label(top, textvariable = self.tiempo)
        self.lbTiempo.grid(row = 0, column = 0)
        self.carita = StringVar()
        self.carita.set(":-)")
        self.btCarita = Button(top, textvariable = self.carita)
        self.btCarita.bind("<Button-1>", self.reiniciar)
        self.btCarita.bind("<ButtonRelease-1>", self.reiniciar)
        self.btCarita.grid(row = 0, column = 1)
        self.cantMAct = StringVar()
        self.actualizarCantM()
        self.lbMinas = Label(top, textvariable = self.cantMAct)
        self.lbMinas.grid(row = 0, column = 2)
        self.fBotones = Frame(top)
        self.fBotones.grid(row = 1, column = 0, columnspan = 3)
        self.botones = []
        for i in range(self.cantx):
            temp = []
            for j in range(self.canty):
                txTemp = StringVar()
                btTemp = Button(self.fBotones, width = 1, textvariable = txTemp)
                btTemp.idx = i
                btTemp.idy = j
                btTemp.bind("<ButtonRelease-1>", self.pisada)
                btTemp.bind("<ButtonRelease-3>", self.pisada)
                btTemp.grid(row = i, column = j)
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
        valor = self.botones[idx][idy][1].get()
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
            self.botones[idx][idy][1].set(valor)
            if valor == "0":
                self.carita.set(":-o")
                # print("{}, {} es 0!!".format(idx, idy))
                self.mostrarCeros(idx,idy)
                self.carita.set(":-)")
            if self.cantp == ((self.cantx * self.canty) - self.cantm):
                self.encurso = False
                self.bloqueado = True
                showinfo("Busca Minas", "Lo has logrado tío! Contratulaciones!")
        elif event.num == 3:
            if valor == "X":
                valor = ""
                self.posibles -= 1
            elif valor == "":
                valor = "X"
                self.posibles += 1
            self.actualizarCantM()
            self.botones[idx][idy][1].set(valor)

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
            valor = self.botones[x][y][1].get()
            if valor == "X":
                valor = "#"
            else:
                valor = "*"
            self.botones[x][y][1].set(valor)

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
                self.botones[i][j][1].set("")

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
                and (self.botones[vx][vy][1].get() == "")):
                self.cantp += 1
                # print("contando {}, {}".format(vx, vy))
                cont = self.contarMinas(vx, vy)
                if cont == 0:
                    # print("{}, {} es 0!!".format(vx, vy))
                    # input()
                    self.botones[vx][vy][1].set(str(cont))
                    self.mostrarCeros(vx, vy)
                else:
                    self.botones[vx][vy][1].set(str(cont))
                    
    def iniciarReloj(self):
        self.tinicio = datetime.datetime.now()
        self.actualizarReloj()
    
    def actualizarReloj(self):
        tactual = datetime.datetime.now() - self.tinicio
        self.tiempo.set("{:02}:{:02}".format(
            tactual.seconds // 60, tactual.seconds % 60))
        if self.encurso:
            self.after(500, self.actualizarReloj)
        
app = BuscaMinas()
app.master.title("Busca Minas")
app.mainloop()
