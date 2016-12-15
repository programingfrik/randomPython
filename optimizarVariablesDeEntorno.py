#!/usr/bin/python3

import re

# Esto es un script para optimizar las variables de entorno que se encuentren dentro de un bat de windows. Optimizar en este caso es obtener las mismas variables con los mismos valores, con el menor número de caracteres en los fuentes del fichero bat. La forma en la que se hace esta optimización es haciendo sustituciones de variables para acortar los valores que hay que poner en los ficheros bat.

pila = []
def proximaVariable(valor, pos):
    """Extrae la próxima "%variable%" de valor después pos.
Extrae la próxima variable de entorno que esté en la forma "%variable%" dentro de la cadena valor después de la posición pos. Retorna un par de valores, la posición después de la variable encontrada para una futura búsqueda y el nombre en mayúscula de la variable encontrada."""
    inicio = valor.find("%", pos)
    fin = valor.find("%", inicio + 1)
    return fin + 1, valor[inicio + 1:fin].upper()

def expandirUna(variable, variables, pila):
    """Expande recursivamente una variable de entorno.
Expande recursivamente una variable de entorno variable tomando en cuenta los valores en el diccionario variables y evitando problemas como una posible referencia circular usando la lista pila para saber cuales variables se han mandado a expandir ya."""
    # print ("Expandiendo {}".format(variable))
    valor = variables[variable]
    pos = 0
    while valor.find("%", pos) != -1:
        pos, referencia = proximaVariable(valor, pos)
        if ((referencia == variable) or (referencia in pila)
            or (not referencia in variables.keys())):
            continue
        if "%" in variables[referencia]:
            expandirUna(referencia, variables, pila)
        # print ("Voy a reemplazar \"{}\" con \"{}\" en \"{}\"".format(
        #     re.escape("%{}%".format(referencia)),
        #     variables[referencia].replace("\\", "\\\\"),
        #     valor))
        valor = re.sub(re.escape("%{}%".format(referencia)),
                       variables[referencia].replace("\\", "\\\\"),
                       valor, flags = re.IGNORECASE)
        # print ("El resultado de la sustitución \"{}\"".format(valor))
    variables[variable] = valor

def expandir(variables):
    """Expande todas las variables en el diccionario variables.
Expande todas las variables en el diccionario variables usando para cada variable expandirUna."""
    for key in variables.keys():
        if "%" in variables[key]:
            expandirUna(key, variables, pila)

def optimizar(variables):
    """Optimiza las variables de entorno.
Hace la mayor cantidad de optimizaciones que pueda para que el eventual bat file sea lo mas pequeño posible."""
    utiles = []
    for variable in variables.keys():
        if len(variables[variable]) > (len(variable) + 2):
            utiles.append(variable)
    utiles = [(len(variables[variable]) - len(variable), i, variable) for i, variable in enumerate(utiles)]
    utiles.sort()
    utiles = [variable for puntos, num, variable in utiles]
    for vutil in utiles:
        for variable in variables.keys():
            if variable == vutil:
                continue
            valorU = variables[vutil]
            valorV = variables[variable]
            if len(valorV) >= len(valorU):
                valorV = valorV.replace(valorU, "%{}%".format(vutil))
                variables[variable] = valorV

def comparar(variables1, variables2):
    """Asumiendo que variables1 y variables2 tienen lo mismo los compara.
Imprime todas las variables linea por linea una con la otra con el tamaño del texto para facilitar la comparación de forma visual."""
    for variable in variables1.keys():
        print ("{0} {1:05} {2}\n{0} {3:05} {4}".format(
            variable, len(variables1[variable]), variables1[variable],
            len(variables2[variable]), variables2[variable]))

def leerBat(fichero):
    """Lee un bat, retorna variables encontradas en un diccionario.
Lee un fichero bat y las variables de entorno que encuentra las pone en un diccionario. Cuando termina con el fichero retorna el diccionario."""
    expVar = re.compile("^ *set *(\w+)=(.+)$", re.IGNORECASE)
    variables = {}
    with open(fichero, "r") as of:
        linea = of.readline()
        while linea != "":
            parecido = expVar.match(linea)
            if parecido:
                variables[parecido.group(1).upper()] = parecido.group(2)
            linea = of.readline()
    return variables

def escribirBat(fichero, variables):
    """Escribe el diccionario de variables en el fichero indicado.
Toma el diccionario de variables y lo escribe en el fichero bat indicado en forma de declaraciones de variables."""
    nombres = list(variables.keys())
    nombres.sort()
    nombresD = nombres.copy()
    for variable in nombres:
        # print (nombresD)
        # print ("Bregando con la variable {}".format(variable))
        valor = variables[variable]
        pos = 0
        while valor.find("%", pos) != -1:
            pos, referencia = proximaVariable(valor, pos)
            # print ("Comparando con la variable {}".format(referencia))
            if (referencia == variable) or (not referencia in variables.keys()):
                continue
            ir = nombresD.index(referencia)
            iv = nombresD.index(variable)
            # print ("{} indice de la referencia y {} indice de la variable".format(ir, iv))
            if iv < ir:
                # print ("{} debe ir antes de {}".format(referencia, variable))
                nombresD.remove(variable)
                nombresD.insert(ir, variable)
    with open(fichero, "w") as of:
        for variable in nombresD:
            of.write("set {}={}\n".format(variable, variables[variable]))
    
