import os
import math
import pygame

RUTA_BASE = "assets/images/decoraciones"

# Decoraciones que llevan un efecto de "brillo pulsante": no son frames
# de animación (un solo PNG alcanza), es el alpha de la imagen oscilando
# con el tiempo, para dar sensación de luz prendida sin tener que pedir
# ni cargar varias imágenes.
_PARPADEAN = {"luces"}

_cache_imagenes = {}


def _cargar_imagen(nombre, tam_casilla):
    clave = (nombre, tam_casilla)
    if clave in _cache_imagenes:
        return _cache_imagenes[clave]

    ruta = os.path.join(RUTA_BASE, f"{nombre}.png")
    if not os.path.exists(ruta):
        _cache_imagenes[clave] = None
        return None

    imagen = pygame.image.load(ruta).convert_alpha()

    # Se escala para que el ANCHO ocupe una casilla (igual que los
    # tiles), pero respetando la proporción del alto: así una
    # estantería de libros puede verse más alta que una casilla sin
    # deformarse, igual que se escalan los personajes en
    # sprites_personajes.py.
    escala = tam_casilla / imagen.get_width()
    ancho_nuevo = tam_casilla
    alto_nuevo = int(imagen.get_height() * escala)

    imagen_escalada = pygame.transform.smoothscale(imagen, (ancho_nuevo, alto_nuevo))
    _cache_imagenes[clave] = imagen_escalada
    return imagen_escalada


def dibujar_decoraciones(hoja_mapa, lista_decoraciones, tam_casilla):
    """lista_decoraciones: lista de (fila, columna, nombre).

    IMPORTANTE: esta función es puramente visual. Nunca se consulta acá
    ni en ningún otro lado para saber si el jugador puede pasar por una
    celda - eso lo sigue decidiendo únicamente self.mapa en jugador.py.
    Así evitamos exactamente el problema de desfasaje que tuvimos con
    el fondo: la colisión y el dibujo de decoraciones son cosas
    completamente separadas a propósito.

    Cada decoración se ancla ABAJO en su casilla (fila, columna), igual
    que los personajes, para que las que son más altas que una casilla
    "crezcan" hacia arriba en vez de hundirse en el piso - por eso las
    posiciones de más abajo se eligieron siempre con una pared arriba:
    así quedan pegadas/montadas contra esa pared en vez de flotando
    solas en medio de un pasillo transitable.
    """

    for fila, columna, nombre in lista_decoraciones:
        imagen = _cargar_imagen(nombre, tam_casilla)
        if imagen is None:
            continue  # todavía no subieron ese archivo: se omite sin romper nada

        x = columna * tam_casilla
        y_pie = fila * tam_casilla + tam_casilla

        superficie = imagen
        if nombre in _PARPADEAN:
            # copy() porque set_alpha no debe pisar la imagen que está
            # cacheada (se reusa en todos los frames siguientes).
            superficie = imagen.copy()
            t = pygame.time.get_ticks() / 400
            alpha = int(197 + 58 * math.sin(t))
            superficie.set_alpha(alpha)

        hoja_mapa.blit(superficie, (x, y_pie - superficie.get_height()))


# ---------------------------------------------------------------------
# Ubicaciones de decoraciones por nivel: (fila, columna, nombre).
# nombre debe tener un archivo en assets/images/decoraciones/<nombre>.png
#
# Elegidas automáticamente con un script que recorre cada mapa de
# niveles.py y selecciona celdas de PISO LIBRE (nunca pared, ítem,
# compuerta, ni posición inicial de P/C/S) que además tienen una PARED
# justo arriba - así, combinado con el anclado-abajo de
# dibujar_decoraciones, cada decoración queda pegada contra esa pared
# en vez de en medio de un pasillo. Se espaciaron para que no queden
# 3 juntas amontonadas en la misma zona, e incluyen también el último
# pasillo de cada nivel (antes solo se llenaba la mitad de arriba).
#
# Son un punto de partida prolijo, no algo definitivo: si alguna te
# tapa un pasillo angosto o te queda fea, es solo cambiar esos dos
# números (fila, columna) de esa línea.
# ---------------------------------------------------------------------

DECORACIONES_NIVEL1 = [
    (1, 2, "pizarra"),
    (1, 6, "libros"),
    (1, 10, "planta"),
    (1, 13, "compu"),
    (3, 2, "luces"),
    (3, 5, "pizarra"),
    (3, 9, "libros"),
    (3, 12, "planta"),
    (5, 1, "compu"),
    (5, 4, "luces"),
    (7, 2, "compu"),
    (7, 5, "pizarra"),
    (7, 8, "libros"),
    (7, 12, "luces"),
]

DECORACIONES_NIVEL2 = [
    (1, 3, "pizarra"),
    (1, 6, "libros"),
    (1, 9, "planta"),
    (1, 13, "compu"),
    (3, 2, "luces"),
    (3, 5, "pizarra"),
    (3, 10, "libros"),
    (5, 1, "planta"),
    (5, 4, "compu"),
    (5, 10, "luces"),
    (7, 2, "pizarra"),
    (7, 6, "libros"),
    (7, 11, "luces"),
]

DECORACIONES_NIVEL3 = [
    (1, 3, "pizarra"),
    (1, 7, "libros"),
    (1, 11, "planta"),
    (1, 14, "compu"),
    (3, 12, "luces"),
    (5, 2, "pizarra"),
    (5, 8, "libros"),
    (5, 11, "planta"),
    (5, 14, "compu"),
    (7, 4, "luces"),
    (9, 2, "libros"),
    (9, 8, "luces"),
    (9, 12, "planta"),
]

DECORACIONES_NIVEL4 = [
    (1, 3, "pizarra"),
    (1, 6, "libros"),
    (1, 9, "planta"),
    (1, 13, "compu"),
    (1, 16, "luces"),
    (3, 5, "pizarra"),
    (3, 9, "libros"),
    (3, 13, "planta"),
    (3, 16, "compu"),
    (5, 1, "luces"),
    (9, 2, "luces"),
    (9, 11, "planta"),
    (9, 15, "compu"),
]

DECORACIONES_NIVEL5 = [
    (1, 3, "pizarra"),
    (1, 6, "libros"),
    (1, 9, "planta"),
    (1, 12, "compu"),
    (1, 16, "luces"),
    (3, 4, "pizarra"),
    (3, 8, "libros"),
    (3, 11, "planta"),
    (3, 15, "compu"),
    (5, 3, "luces"),
    (11, 2, "planta"),
    (11, 7, "compu"),
    (11, 13, "pizarra"),
]

DECORACIONES_NIVEL6 = [
    (1, 3, "pizarra"),
    (1, 6, "libros"),
    (1, 9, "planta"),
    (1, 12, "compu"),
    (1, 15, "luces"),
    (3, 2, "pizarra"),
    (3, 5, "libros"),
    (3, 8, "planta"),
    (3, 11, "compu"),
    (3, 16, "luces"),
    (11, 4, "compu"),
    (11, 10, "pizarra"),
    (11, 13, "libros"),
    (11, 16, "luces"),
]

DECORACIONES_NIVEL7 = [
    (1, 2, "pizarra"),
    (1, 5, "libros"),
    (1, 8, "planta"),
    (1, 11, "compu"),
    (1, 14, "luces"),
    (1, 18, "pizarra"),
    (3, 1, "libros"),
    (3, 8, "planta"),
    (3, 11, "compu"),
    (3, 18, "luces"),
    (13, 2, "pizarra"),
    (13, 6, "libros"),
    (13, 9, "luces"),
    (13, 12, "planta"),
]

DECORACIONES_NIVEL8 = [
    (1, 3, "pizarra"),
    (1, 6, "libros"),
    (1, 9, "planta"),
    (1, 13, "compu"),
    (1, 16, "luces"),
    (1, 19, "pizarra"),
    (3, 2, "libros"),
    (3, 6, "planta"),
    (3, 9, "compu"),
    (3, 15, "luces"),
    (13, 2, "libros"),
    (13, 8, "luces"),
    (13, 17, "planta"),
    (13, 20, "compu"),
]

DECORACIONES_NIVEL9 = [
    (1, 2, "pizarra"),
    (1, 5, "libros"),
    (1, 10, "planta"),
    (1, 13, "compu"),
    (1, 17, "luces"),
    (1, 20, "pizarra"),
    (3, 1, "libros"),
    (3, 6, "planta"),
    (3, 9, "compu"),
    (3, 12, "luces"),
    (13, 4, "luces"),
    (13, 11, "planta"),
    (13, 16, "compu"),
    (13, 20, "pizarra"),
]

DECORACIONES_NIVEL10 = [
    (1, 3, "pizarra"),
    (1, 7, "libros"),
    (1, 10, "planta"),
    (1, 14, "compu"),
    (1, 17, "luces"),
    (1, 20, "pizarra"),
    (3, 1, "libros"),
    (3, 8, "planta"),
    (3, 13, "compu"),
    (3, 18, "luces"),
    (13, 4, "planta"),
    (13, 9, "compu"),
    (13, 19, "pizarra"),
]

# Índice 0 = nivel1, índice 1 = nivel2, etc. (mismo criterio 0-based
# que usa indice_nivel en estado_jugando.py).
DECORACIONES_POR_NIVEL = {
    0: DECORACIONES_NIVEL1,
    1: DECORACIONES_NIVEL2,
    2: DECORACIONES_NIVEL3,
    3: DECORACIONES_NIVEL4,
    4: DECORACIONES_NIVEL5,
    5: DECORACIONES_NIVEL6,
    6: DECORACIONES_NIVEL7,
    7: DECORACIONES_NIVEL8,
    8: DECORACIONES_NIVEL9,
    9: DECORACIONES_NIVEL10,
}