# Leyenda de caracteres para armar mapas (usada por
# patterns/factory/item_factory.py y por Jugador.mover):
#   #  pared            P  posición inicial del jugador
#   S  salida           C  posición inicial del cazador
#   D  compuerta (necesita 1 llave para abrirse, se abre una sola vez)
#   E  ítem escudo      K  ítem llave
#   V  ítem velocidad (buff)
#   L  ítem lentitud (debuff)      I  ítem invertir controles (debuff)
# Cualquier otro carácter (por ejemplo ".") se dibuja como piso normal.

nivel1 = [

"################",
"#P   K   #    S#",
"# #####D # #####" ,
"#  E   #  V    #",
"###### ######  #",
"#    L      I  #",
"# ####### ######",
"#C             #",
"################"

]