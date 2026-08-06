import pygame
from constantes import *


class Item:
    """
    Clase base para todos los ítems que aparecen en el laberinto.

    Esta es la jerarquía de "productos" del patrón Factory Method:
    el resto del juego (estado_jugando.py) solo trabaja contra esta
    clase base (la dibuja, revisa si el jugador la tocó, le pide que
    aplique su efecto). Nunca necesita saber qué subclase es en
    concreto - eso lo decide la fábrica correspondiente en
    item_factory.py.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLANCO
        self.recolectado = False

    def aplicar_efecto(self, jugador):
        """Cada ítem concreto define acá qué le hace al jugador
        cuando lo recolecta. La clase base no hace nada."""
        pass

    def dibujar(self, pantalla):
        if self.recolectado:
            return

        centro = (
            self.x * TAM_CASILLA + TAM_CASILLA // 2,
            self.y * TAM_CASILLA + TAM_CASILLA // 2
        )
        pygame.draw.circle(pantalla, self.color, centro, TAM_CASILLA // 5)


class ItemEscudo(Item):
    """Protege al jugador: la próxima vez que el cazador lo atrape,
    se consume el escudo en vez de perder una vida."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = CELESTE

    def aplicar_efecto(self, jugador):
        jugador.escudos += 1


class ItemLlave(Item):
    """Se necesita para abrir compuertas (casillas 'D' en el mapa).
    Cada compuerta consume una llave al abrirse."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = AMARILLO

    def aplicar_efecto(self, jugador):
        jugador.llaves += 1


class ItemVelocidad(Item):
    """Buff temporal: mientras está activo, cada movimiento del
    jugador avanza 2 casillas en vez de 1 (si el camino está libre)."""

    DURACION_MS = 6000

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = VERDE_CLARO

    def aplicar_efecto(self, jugador):
        jugador.activar_efecto_temporal("velocidad", self.DURACION_MS)


class ItemLentitud(Item):
    """Perjudicial: mientras está activo, el jugador solo se mueve
    en 1 de cada 2 pulsaciones de tecla (el resto se ignoran)."""

    DURACION_MS = 5000

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = MARRON

    def aplicar_efecto(self, jugador):
        jugador.activar_efecto_temporal("lentitud", self.DURACION_MS)


class ItemInvertir(Item):
    """Perjudicial: mientras está activo, se invierten los controles
    (arriba<->abajo, izquierda<->derecha)."""

    DURACION_MS = 5000

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = VIOLETA

    def aplicar_efecto(self, jugador):
        jugador.activar_efecto_temporal("invertido", self.DURACION_MS)
