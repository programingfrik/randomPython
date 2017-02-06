#!/usr/bin/python3

from turtle import *
from math import *

lado = 100
doble = lado * 2
mitad = lado * 0.5
pequeno = lado * 0.2
pequenoAngulo = (pequeno / sin(radians(45)))
interior = lado - (pequeno * 2)
dobleInterior = doble - (pequeno * 2)

color1 = "#FF7700"
color2 = "#FFAA00"
color3 = "#CC3300"

right(90)
forward(mitad)

color(color1)
begin_fill()
forward(lado)
right(90)
forward(lado)
right(90)
forward(doble)
right(90)
forward(lado)
left(90)
forward(lado)
right(90)
forward(lado)
right(90)
forward(doble)
right(90)
forward(lado)
end_fill()

right(90)

color(color3)
begin_fill()
left(45)
forward(pequenoAngulo)
right(135)
forward(lado)
right(45)
forward(pequenoAngulo)
right(135)
forward(lado)
end_fill()

right(180)
forward(lado)
left(90)

color(color2)
begin_fill()
forward(doble)
left(90)
forward(lado)
left(135)
forward(pequenoAngulo)
left(45)
forward(interior)
right(90)
forward(dobleInterior)
left(45)
forward(pequenoAngulo)
end_fill()

left(135)
forward(doble)
left(90)
forward(lado)
left(90)

color(color3)
begin_fill()
forward(lado)
left(45)
forward(pequenoAngulo)
left(135)
forward(lado)
left(45)
forward(pequenoAngulo)
end_fill()

left(135)
forward(lado)

color(color2)
begin_fill()
left(45)
forward(pequenoAngulo)
right(135)
forward(lado)
right(45)
forward(pequenoAngulo)
right(135)
forward(lado)
end_fill()

right(180)
forward(lado)
left(90)

color(color3)
begin_fill()
forward(doble)
left(90)
forward(lado)
left(135)
forward(pequenoAngulo)
left(45)
forward(interior)
right(90)
forward(dobleInterior)
left(45)
forward(pequenoAngulo)
end_fill()

left(135)
forward(doble)
left(90)
forward(lado)
left(90)

color(color2)
begin_fill()
forward(lado)
left(45)
forward(pequenoAngulo)
left(135)
forward(lado)
left(45)
forward(pequenoAngulo)
end_fill()

done()
