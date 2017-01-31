#!/usr/bin/python3

# El triangulo de sierpinski

from tkinter import *
import datetime

class Sierpinski(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(sticky = N + S + E + W)
        self.crearControles()

    def crearControles(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight = 1)
        top.columnconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.lbTriangulo = Label(self, text = "Triángulo")
        self.lbTriangulo.grid(row = 0, column = 0)
        self.txTriangulo = Text(self, height = 1, width = 30)
        self.txTriangulo.grid(row = 0, column = 1)
        self.txTriangulo.insert(INSERT, "((150, 0), (0, 300), (300, 300))")
        self.rowconfigure(1, weight = 1)
        self.lbEtapa = Label(self, text = "Etapa")
        self.lbEtapa.grid(row = 1, column = 0)
        self.txEtapa = Text(self, height = 1, width = 10)
        self.txEtapa.grid(row = 1, column = 1)
        self.txEtapa.insert(INSERT, "3")
        self.rowconfigure(2, weight = 1)
        self.btDibujar = Button(self, text = "Dibujar !!", command = self.hacerDibujo)
        self.btDibujar.grid(row = 2, column = 1)
        self.rowconfigure(3, weight = 1)
        self.cvDibujo = Canvas(self, height = 300, width = 300)
        self.cvDibujo.grid(row = 3, column = 0, columnspan = 2)
        
    def hacerDibujo(self):
        tgls = []
        # borrar todo lo que haya en el canvas
        objetos = self.cvDibujo.find_all()
        for objeto in objetos:
            self.cvDibujo.delete(objeto)
        # trae los datos del formulario
        tgls.append(eval(self.txTriangulo.get("1.0", END)))
        etapas = int(self.txEtapa.get("1.0", END))
        # subdivide la cantidad de veces necesarias
        # print(tgls)
        while etapas > 0:
            nuevo = []
            for tgl in tgls:
                nuevo.extend(subdividir(tgl))
            tgls = nuevo
            # print(tgls)
            etapas -= 1
        # haz el dibujo
        for tgl in tgls:
            self.cvDibujo.create_polygon(tgl[0][0], tgl[0][1], tgl[1][0], tgl[1][1], tgl[2][0], tgl[2][1])
        pass

def subdividir(tgl):
    a = tgl[0]
    b = tgl[1]
    c = tgl[2]
    ab = puntoMedio(a, b)
    bc = puntoMedio(b, c)
    ca = puntoMedio(c, a)
    return [(a, ab, ca), (ab, b, bc), (ca, bc, c)]
    
def puntoMedio(a, b):
    x = (a[0] + b[0]) // 2
    y = (a[1] + b[1]) // 2
    # print("Punto medio {}, {}, {}, {}".format(a, b, x, y))
    return x, y
    
app = Sierpinski()
app.master.title("Triangulo de Sierpinski")
app.mainloop()
