import os
import pygame

# Cada carácter de la matriz de niveles.py se asocia a un archivo de tile.
# Si el archivo no existe todavía (por ejemplo, mientras vas generando las
# imágenes de a poco), se usa un color sólido de respaldo para que el
# juego siga andando sin romperse.
_ARCHIVOS_TILE = {
    "#": "assets/images/tiles/pared.png",
    "S": "assets/images/tiles/salida.png",
    "D": "assets/images/tiles/puerta.png",
    ".": "assets/images/tiles/piso.png",  # piso normal (y default)
}

# Colores de respaldo (los mismos que se usaban antes), por si falta
# algún archivo de tile.
from constantes import GRIS, VERDE, MARRON_OSCURO, BLANCO

_COLORES_RESPALDO = {
    "#": GRIS,
    "S": VERDE,
    "D": MARRON_OSCURO,
    ".": BLANCO,
}

# Cache: {(caracter, tam_casilla): pygame.Surface}. Escalar imágenes
# es una operación relativamente cara, así que no queremos hacerlo
# en cada frame ni tampoco recargar el archivo del disco cada vez.
_cache_tiles = {}


def obtener_tile(caracter, tam_casilla):
    """Devuelve una Surface de tam_casilla x tam_casilla para el carácter
    dado ('#', 'S', 'D', o cualquier otro que se trate como piso). Si la
    imagen no existe en disco, devuelve None (quien llama debe usar el
    color de respaldo con pygame.draw.rect en ese caso)."""

    clave_mapa = caracter if caracter in _ARCHIVOS_TILE else "."
    clave_cache = (clave_mapa, tam_casilla)

    if clave_cache in _cache_tiles:
        return _cache_tiles[clave_cache]

    ruta = _ARCHIVOS_TILE[clave_mapa]

    if not os.path.exists(ruta):
        _cache_tiles[clave_cache] = None
        return None

    imagen = pygame.image.load(ruta).convert_alpha()
    imagen_escalada = pygame.transform.smoothscale(
        imagen, (tam_casilla, tam_casilla)
    )
    _cache_tiles[clave_cache] = imagen_escalada
    return imagen_escalada


def color_respaldo(caracter):
    clave_mapa = caracter if caracter in _COLORES_RESPALDO else "."
    return _COLORES_RESPALDO[clave_mapa]