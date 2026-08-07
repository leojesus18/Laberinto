# Leyenda de caracteres para armar mapas (usada por
# patterns/factory/item_factory.py y por Jugador.mover):
#   #  pared            P  posición inicial del jugador
#   S  salida           C  posición inicial del cazador
#   D  compuerta (necesita 1 llave para abrirse, se abre una sola vez)
#   E  ítem escudo      K  ítem llave
#   V  ítem velocidad 
#   L  ítem lentitud 
#   I  ítem invertir controles 
# Cualquier otro carácter (por ejemplo ".") se dibuja como piso normal.

# Nivel 1: es el tutorial/nivel fácil. Tiene ítems "buenos" (escudo,
# llave, velocidad) y UNA compuerta para que se entienda la mecánica,
# pero SIN ítems perjudiciales (lentitud/invertir) - esos arrancan
# recién en los niveles más difíciles, para no confundir en el primero.
nivel1 = [

"################",
"#P   K   #    S#",
"# #####D # #####" ,
"#  E   #  V    #",
"###### ######  #",
"#              #",
"# ####### ######",
"#C             #",
"################"

]