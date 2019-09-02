#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Un programa de consola para repartir una factura de almuerzo o algo parecido entre varias personas.
# Las funcionalidades que se espera que esto tenga:
# - Tiene que tener en cuenta que la factura podría estar en valor de precio por unidad o precio total.
# - Tiene que tener en cuenta que una o más personas pueden ser cumpleañeros y sus subcuentas tienen que dividirse entre las demás personas.
# - Tiene que permitir agregar o quitar elementos de la factura.
# - Tiene que permitir agregar o quitar personas de las subcuentas.
# - Tiene que sacar los impuestos de cada cuenta.
# - Tiene que imprimir cada factura de forma entendible.
# - Tiene que poder leer su información de facturación y distribución de un solo fichero.
# - Tiene que ser usable desde la consola de python, importable en forma de un módulo.
#
# Cosas deseables:
# - Que envíe la cuenta a través del correo.

# Esta es la segunda versión porque antes hice un intento que se llama distribucionCumpleano.py

# Este es el programa que va a hacer que los amigos de la oficina amen de nuevo la consola y el super lenguaje de programación python. Está pensado para que sea fácil de editar de entender y manipular.


import sys
import manejoEntradas

class articulo:
    def __init__(self, nombre, cantidad, precio, esUnitario = False):
        self.numero = 0
        self.nombre = nombre
        self.cantidad = cantidad
        if esUnitario:
            self.precio = precio
        else:
            self.precio = precio / self.cantidad
    def calcularTotal(self):
        return self.precio * self.cantidad

class factura:
    def __init__(self):
        self.articulos = []
        self.impuesto = 0.0
        self.preciosUnitarios = False
    def imprimir(self):
        total = 0.0
        festejado = 0.0
        impuestos = 0.0
        print("Número Nombre                    Cantidad             Precio")
        print("------ ------------------------- -------- ------------------")
        for art in self.articulos:
            print("{0: >6} {1: <25} {2: >8} {3: >18.2f}".format(art.numero, art.nombre, art.cantidad, art.precio))
            total += art.cantidad * art.precio
        print("       -----------------------------------------------------")
        if festejado > 0.0:
            print("       aporte festejado                   {0: >18.2f}".format(festejado))
        
        print("       Sub-Total                          {0: >18.2f}".format(total))
        impuestos = (total * self.impuesto) / 100
        print("       Impuestos                          {0: >18.2f}".format(impuestos))
        total += impuestos
        print("       Total                              {0: >18.2f}".format(total))

class distribucion:
    """Una instancia de esta clase representa el estado del programa."""
    def __init__(self):
        self.fichero = ""
        self.factura = ""
        self.cumpleaneros = []
        self.personas = []
        self.subfacturas = {}
        self.cambios = False

    def escribir(self):

        if self.fichero == "":
            print("No se puede escribir, no tengo un nombre de fichero")
            return
        
        pass

    def leer(self):

        if self.fichero == "":
            print("No se puede leer, no tengo un nombre de fichero")
            return
        
        pass
    
def captura(mensaje):
    respondida = False
    while not respondida:
        valor = input(mensaje + "(menu = ir a menu principal)")
        if valor == "menu":
            menuPrincipal()
        else:
            respondida = True
    return valor
        
def capturarFichero():
    fichero = capturar("¿Cual es el nombre del fichero para esta cuenta?(en blanco = no salvar)")
    return fichero

def capturarListaArticulos(previos):
    return None

def eliminarArticulo(previos):
    return None

def capturarFactura():
    opc = 0
    opciones = ["introducir impuesto", "introducir si es precio unitario", "agregar items", "eliminar items", "factura lista"]
    lafactura = factura()
    lafactura.impuesto = leerEntradaEnteroRango("¿Cual es el valor del impuesto?", 0, 100, 28)
    lafactura.preciosUnitarios = leerEntradaSiNo("¿La factura tiene precios unitarios?")
    lafactura.articulos = capturarListaArticulos()
    
    while opc != 5:
        opc = leerEntradaOpcion(opciones, "Elige una opción")
        if opc == 1:
            lafactura.impuesto = leerEntradaEnteroRango("¿Cual es el valor del impuesto?", 0, 100, 28)
        elif opc == 2:
            lafactura.preciosUnitarios = leerEntradaSiNo("¿La factura tiene precios unitarios?")
        elif opc == 3:
            lafactura.articulos = capturarListaArticulos(lafactura.articulos)
        elif opc == 4:
            lafactura.articulos = eliminarArticulos(lafactura.articulos)
    
    return lafactura

def menuPrincipal(esSubMenu = True):
    global ladist
    
    print("Menú principal")
    
    opciones = ["nombre fichero", "introducir factura",
                "introducir cumpleañeros", "introducir otras personas",
                "hacer distribución", "leer fichero", "escribir fichero", "salir"]
    leerEntradaOpcion(opciones, "Elige una opción")
    
    if esSubMenu:
        opciones.append("Cancelar")
    
    if sel = 0:
        ladist.fichero = capturarFichero()
    elif sel = 1:
        ladist.factura = capturarFactura()
    elif sel == 2:
        ladist.cumpleaneros = capturarPersonas()
    elif sel == 3:
        ladist.personas = capturarPersonas()
    elif sel = 4:
        ladist.subfacturas = hacerDistribucion()
    elif sel == 5:
        ladist.leer()
    elif sel == 6:
        ladist.escribir()
    elif sel == 7:
        sys.exit(0)
    elif sel == 8:
        return
    pass

def modoWizard():
    global ladist
    
    print ("Modo Wizard")
    
    ladist.fichero = capturarFichero()
    
    ladist.factura = capturarFactura()
    
    ladist.cumpleaneros = capturarPersonas()
    
    ladist.personas = capturarPersonas()
    
    ladist.subfacturas = hacerDistribucion()
    
    print("¿Desea hacer algo más o salir? (No = salir/si = mostrar menú principal)")
    if (resp = "si"):
        menuPrincipal(False)

ladist = distribucion()
        
modoWizard()

// menuPrincipal(False)
