#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Como siempre tenemos que hacer distribuciones de cuentas de
# cumpleaños y esas cosas, este es un script para hace la distribución
# de una cuenta de un cumpleañero.

import sys
import math

formatofact1 = "Número Nombre                    Cantidad             Precio"
formatofact2 = "------ ------------------------- -------- ------------------"
formatofact3 = "{0: >6} {1: <25} {2: >8} {3: >18.2f}"
formatofact4 = "       -----------------------------------------------------"
formatofact5 = "       aporte festejado                   {0: >18.2f}"
formatofact6 = "       Sub-Total                          {0: >18.2f}"
formatofact7 = "       Impuestos + Propina                {0: >18.2f}"
formatofact8 = "       Total                              {0: >18.2f}"

def copiardict(valor):
    return dict([(k, v[:]) for k, v in valor.items()])

def capturarmonto(mensaje):
    try:
        resp = input(mensaje)
        resp = float(resp)
    except ValueError:
        return None
    return resp

def capturarItem(numero):
    print ("Para este item #{0} Introduzca:".format(numero))

    resp = input ("Nombre del item (en blanco para terminar): ")
    if (len(resp.strip()) == 0):
        return None
    nombre = resp
    
    cantidad = 1
    resp = input ("Cantidad de ese item o en blanco para uno: ")
    if (resp.isdigit()):
        cantidad = int(resp)

    prompt = "Precio para este item: "
    precio = capturarmonto(prompt)
    while not precio:
        precio = capturarmonto("Error! " + prompt)

    print ("Listo !")
    return [nombre, cantidad, precio]

def mostrarfactura(factura, manejador = None):
    subtotal = 0
    ponermensaje (formatofact1, manejador)
    ponermensaje (formatofact2, manejador)
    for item in factura:
        subtotal += factura[item][1] * factura[item][2]
        ponermensaje (formatofact3.format(
            item, factura[item][0], factura[item][1],
            factura[item][2]), manejador)
    return subtotal

def opciones(numeronombre):
    keys = []
    for numero, nombre in numeronombre:
        keys.append(str(numero))
        print ("{0} - {1}".format(numero, nombre))

    prompt = "Opción (en blanco para terminar): "
    resp = input(prompt)
    while (resp.strip() != "") and not(resp in keys):
        resp = input("Error! " + prompt)
    if (len(resp) == 0):
        return None
    else:
        return int(resp)

def capturaritempersona(factura):
    print("Elija un item:")
    items = [(i, "{0: <25} {1: >8}".format(factura[i][0], factura[i][1]))
             for i in factura if factura[i][1] > 0]
    resp = opciones(items)
    return resp

def capturarcantidad(max, inicial=1):
    prompt = "Cantidad entre 1 y {0} (en blanco es {1}):".format(max, inicial)
    resp = input(prompt)
    while ((resp != "") and (not(resp.isdigit())
                             or (int(resp) < 1)
                             or (int(resp) > max))):
        resp = input("Error!: " + prompt)
    if resp != "":
        return int(resp)
    return inicial
    
def capturarpersona(nombres, factura):
    nombre = input("Nombre:")
    while nombre in nombres:
        nombre = input("Ese nombre ya existe, introduzca otro: ")
    items = []
    print("Introduzca las cosas consumio {0}:".format(nombre))
    resp = capturaritempersona(factura)
    # TODO: cuando se hace captura de items, si se pide por separado dos items que son lo mismo hay que sumarlos
    while resp:
        cantidad = capturarcantidad(factura[resp][1])
        factura[resp][1] -= cantidad
        items.append((resp, cantidad))
        print ("Listo !")
        resp = capturaritempersona(factura)
        # TODO: tiene que permitir personas sin items.
        # TODO: Inmediatamente se acaban los items ya no hay mas nada que repartir y no hay que preguntarle nada al usuario, simplemente salir.
    return nombre, items

def eliminarpersona(personas, factura, nombre):
    for item, cantidad in personas[nombre]:
        factura[item][1] += cantidad
    del(personas[nombre])

def facturapersona(nombre, personas, factura, manejador = None):
    ponermensaje("\nLa subfactura de {0}: ".format(nombre), manejador)
    subtotal = 0
    ponermensaje(formatofact1,manejador)
    ponermensaje(formatofact2,manejador)
    for item, cantidad in personas[nombre]:
        subtotal += cantidad * factura[item][2]
        ponermensaje(formatofact3.format(
            item, factura[item][0], cantidad, factura[item][2]), manejador)
    return subtotal

def mostrartotal(subtotal, impuestos, cantidad = 0,
                 adicional = 0, manejador=None):
    ponermensaje(formatofact4, manejador)
    if cantidad and adicional:
        ponermensaje(formatofact5.format(adicional / cantidad), manejador)
        subtotal += adicional / cantidad
    ponermensaje(formatofact6.format(subtotal), manejador)
    totalimpuestos = (subtotal * impuestos) / 100
    ponermensaje(formatofact7.format(totalimpuestos), manejador)
    total = subtotal + totalimpuestos
    ponermensaje(formatofact8.format(total), manejador)
    return total

def ponermensaje(texto, destino = None):
    print(texto)
    if destino:
        destino.write(texto + "\n")

# la representación de la factura
facturao = {}

print ("Distribución de cuenta de cumpleaños")

# TODO: El programa puede parsear el fichero que tiene una factura previa y modificarla agregandole o quitandole cosas a la factura y tal vez re-haciendo la distribución. En el momento en que se modifica la factura hay que destruir la distribución previa porque si no no va a coincidir.
fichero = input ("¿Nombre del fichero para salvar la factura? "
                 + "(en blanco = no salvar)")
manejador = None
if (fichero != ""):
    manejador = open(fichero, "w")

print ("Introduciendo la factura")

# Lo primero es introducir la factura un item a la vez

estotal = True
resp = input("La factura tiene el total del item o el precio"
             + " por unidad [S=total/n=unidad]:")
if ((len(resp) > 0) and (resp[0] == "n")):
    estotal = False

print ("¿Qué porcentaje de impuestos + propina?")
impuestos = capturarcantidad(100, 28)

# Para cada item de la factura
cont = 1
resp = "I"
while (len(resp) > 0) and (resp.upper()[0] != "L"):
    resp = resp.upper()[0]
    if (resp == "I"):
        print ("Introduciendo items:")
        item = capturarItem(cont)
        while (item):
            facturao[cont] = item
            # TODO: Se pueden asignar los números después que se hayan ingresando todos los items y así evitar que estén discontinuos.
            cont += 1    
            item = capturarItem(cont)
    elif (resp == "E"):
        print("¿Que item deseas eliminar?")
        num = opciones([(num, valores[0])
                        for num, valores in facturao.items()])
        if num:
            del(facturao[num])
    print ("La factura actual:\n")
    mostrarfactura(facturao)
    resp = input("[I]ntroducir, [E]liminar o [L]isto:")

ponermensaje("\nLa factura original:", manejador)
mostrarfactura(facturao, manejador)

if estotal:
    cpfactura = dict([(i, [facturao[i][0],
                           facturao[i][1],
                           facturao[i][2] / facturao[i][1]]
    ) for i in facturao])
    facturao = copiardict(cpfactura)
else:
    cpfactura = copiardict(facturao)

print ("\nAhora a la repartición:")

cumpleaneros = {}
personas = {}
prompt = "\nIntroducir [P]ersona, [C]umpleañero, [E]liminar "\
         + "persona o [L]isto:"
resp = input(prompt)
while (len(resp) > 0) and (resp.upper()[0] != "L"):
    resp = resp.upper()[0]
    nombres = ([nombre for nombre in cumpleaneros]
               + [nombre for nombre in personas])
    if (resp == "P"):
        print ("Para la persona introduzca:")        
        nombre, persona = capturarpersona(nombres, cpfactura)
        if persona:
            personas[nombre] = persona
    elif(resp == "C"):
        print ("Para el cumpleañero introduzca:")
        nombre, persona = capturarpersona(nombres, cpfactura)
        if persona:
            cumpleaneros[nombre] = persona
    elif(resp == "E"):
        print("¿A que persona deseas eliminar?")
        num = opciones(list(zip(range(len(nombres)), nombres)))
        if (nombres[num] in cumpleaneros.keys()):
            eliminarpersona(cumpleaneros, cpfactura, nombres[num])
        elif (nombres[num] in personas.keys()):
            eliminarpersona(personas, cpfactura, nombres[num])

    print("El estado de la factura:")
    mostrarfactura(cpfactura)
    
    if (cumpleaneros):
        print("Los cumpleañeros actuales:")
        for nombre in cumpleaneros:
            facturapersona(nombre, cumpleaneros, cpfactura)
    else:
        print("No hay cumpleaneros.")

    if (personas):
        print("Las personas actuales:")
        for nombre in personas:
            facturapersona(nombre, personas, cpfactura)            
    else:
        print("No hay personas.")

    # TODO: no puede permitir salir sin consumir todos los valores de la factura
    resp = input(prompt)

ponermensaje("\nLa factura con precios unitarios:", manejador)
    
subtotal = mostrarfactura(facturao, manejador)
totalimpuestos = (subtotal * impuestos) / 100
total = mostrartotal(subtotal, impuestos, manejador=manejador)

subtotales = 0
totalcumpleaneros = 0
if (cumpleaneros):
    ponermensaje ("\nLos cumpleaneros:", manejador)
    for nombre in cumpleaneros:
         subtotal = facturapersona(nombre, cumpleaneros, facturao, manejador)
         subtotales += subtotal
         totalcumpleaneros += mostrartotal(subtotal, impuestos, manejador=manejador)

         ponermensaje ("\nEl total a pagar por los cumpleañeros: {0:.2f}".format(subtotales), manejador)
         ponermensaje ("La repartición: {0:.2f} / {1:.2f} = {2:.2f}.".format(
             subtotales, len(personas), subtotales / len(personas)), manejador)

totalpersonas = 0
if (personas):
    ponermensaje ("\nLas personas:", manejador)
    for nombre in personas:
        subtotal = facturapersona(nombre, personas, facturao, manejador)
        totalpersonas += mostrartotal(subtotal, impuestos, len(personas), subtotales, manejador=manejador)

ponermensaje ("\nEl total a pagar entre todos/as: {0:.2f}".format(totalpersonas), manejador)

if manejador:
    manejador.close()

print ("Todo listo!")
