#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Este programa es un reloj de ajedrez para llevar el tiempo de una partida
# se acciona a través de los botones en la interface gráfica o a través de
# las teclas Shift derecha o izquierda o la barra espaciadora.

# Esto lo hice por petición de un amigo de APEC, Siul Veloz, aunque a él
# nunca le interesó el resultado, aquí esta por si a alguien le interesa.

from Tkinter import *
import tkFont
import datetime

class RelojAjedrez(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(sticky = N + S + E + W)
        self.crearControles()

    def crearControles(self):
        top=self.winfo_toplevel()        
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        letrasDisp = tkFont.Font(family = "Courier", size = 20, weight = "bold")
        self.lbTiNegras = Label(self, text = "00:00:00", font = letrasDisp, bg = "#000", fg = "#FFF")
        self.lbTiNegras.grid(row = 0, column = 0)        
        self.lbTiBlancas = Label(self, text = "00:00:00", font = letrasDisp, bg = "#FFF", fg = "#000")
        self.lbTiBlancas.grid(row = 0, column = 1)        
        self.bGNegras = Button(self, text = "Negras", command = self.bGNegrasClick)
        self.bGNegras.grid(row = 1, column = 0)        
        self.bGBlancas = Button(self, text = "Blancas", command = self.bGBlancasClick)
        self.bGBlancas.grid(row = 1, column = 1)        
        self.bind_all("<space>", self.teclasPres)
        self.bind_all("<Shift_L>", self.teclasPres)
        self.bind_all("<Shift_R>", self.teclasPres)        
        self.bGBlancas.grid()
        self.iniciarCont()
        self.mostrarReloj()

    def iniciarCont(self):
        # cantidad de minutos
        cantmin = 5
        # la variable para llevar el reloj Negro
        self.rNegras = datetime.timedelta(minutes = cantmin)
        # la variable para llevar el reloj Blanco
        self.rBlancas = datetime.timedelta(minutes = cantmin)
        # variable para guardar cuando tiempo habia en un reloj
        # al comienzo de la cuenta
        self.dComienzo = datetime.timedelta(minutes = cantmin)
        # variable para tomar tiempos en cada tick y compararlo con
        # el que se toma al inicio del intervalo en referencia
        self.tMuestra = datetime.datetime.min
        # Tiempo que se toma al principio del intervalo para referencia
        self.tReferencia = datetime.datetime.min
        # si es true el reloj referenciado es el blanco si no el negro
        self.refBlancas = False
        # una variable entera para guardar el id que devuelve el after
        # en caso de que se necesite cancelarlo
        self.idTempo = None
        # indica que el reloj esta iniciado y contando
        self.contando = False

    def relojTick(self):
        self.tMuestra = datetime.datetime.now()
        # si el reloj blanco esta seleccionado
        if(self.refBlancas):
            # que descuente tiempo del reloj blanco
            self.rBlancas = self.dComienzo - (self.tMuestra - self.tReferencia)
            if self.rBlancas <= datetime.timedelta(0):
                self.rBlancas = datetime.timedelta(0)
                self.idTempo = None
                self.contando = False
            else:
                self.idTempo = self.after(100, self.relojTick)
        else:
            # si no que descuente del reloj negro
            self.rNegras = self.dComienzo - (self.tMuestra - self.tReferencia)
            if self.rNegras <= datetime.timedelta(0):
                self.rNegras = datetime.timedelta(0)
                self.idTempo = None
                self.contando = False
            else:
                self.idTempo = self.after(100, self.relojTick)
        self.mostrarReloj()
    
    def mostrarReloj(self):
        self.lbTiNegras.config(text = "%02d:%02d:%02d" %(self.rNegras.seconds / 60
                                                        ,self.rNegras.seconds % 60
                                                        ,self.rNegras.microseconds / 10000))
        self.lbTiBlancas.config(text = "%02d:%02d:%02d" %(self.rBlancas.seconds / 60
                                                        ,self.rBlancas.seconds % 60
                                                        ,self.rBlancas.microseconds / 10000))
    
    def detenerBlancas(self, detenerRBlanco):
        # si alguno de los relojes no tiene tiempo
        if (self.rBlancas <= datetime.timedelta(0)) or (self.rBlancas <= datetime.timedelta(0)):
            self.iniciarCont()
        # si me piden detener el reloj blanco
        if detenerRBlanco and (not self.contando or (self.contando and self.refBlancas)):
            # si hay un reloj activado que lo detenga
            if self.idTempo != None:
                self.after_cancel(self.idTempo)
            # que detenga el reloj blanco
            self.rBlancas = self.dComienzo - (self.tMuestra - self.tReferencia)
            # y que inicie el reloj negro
            self.dComienzo = self.rNegras
            self.tMuestra = self.tReferencia = datetime.datetime.now()
            self.refBlancas = False
        # si me piden detener el reloj negro
        elif not detenerRBlanco and (not self.contando or (self.contando and not self.refBlancas)):
            # si hay un reloj activado que lo detenga
            if self.idTempo != None:
                self.after_cancel(self.idTempo)
            # que detenga el reloj negro
            self.rNegras = self.dComienzo - (self.tMuestra - self.tReferencia)
            # y que inicie el reloj blanco
            self.dComienzo = self.rBlancas
            self.tMuestra = self.tReferencia = datetime.datetime.now()            
            self.refBlancas = True
        else:
            return
        # ahora estamos contando
        self.contando = True
        # hay que poner a correr el reloj
        self.idTempo = self.after(100, self.relojTick)

    def bGNegrasClick(self):        
        self.detenerBlancas(False)

    def bGBlancasClick(self):
        self.detenerBlancas(True)

    def teclasPres(self, event):
        if (event.keysym == "space"):
            self.detenerBlancas(self.refBlancas)
        elif (event.keysym == "Shift_L"):
            self.detenerBlancas(False)
        elif (event.keysym == "Shift_R"):
            self.detenerBlancas(True)

app = RelojAjedrez()
app.master.title("Reloj de Ajedrez")
app.mainloop()
