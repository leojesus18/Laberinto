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
        self.puntos = 0  # cuánto suma al puntaje al recolectarlo

    def aplicar_efecto(self, jugador):
        """Cada ítem concreto define acá qué le hace al jugador
        cuando lo recolecta. La clase base no hace nada."""
        pass

    def _centro(self):
        return (
            self.x * TAM_CASILLA + TAM_CASILLA // 2,
            self.y * TAM_CASILLA + TAM_CASILLA // 2
        )

    def dibujar(self, pantalla):
        """Por defecto dibuja un círculo simple. Cada ítem concreto
        sobreescribe esto con una forma que se reconozca de un vistazo,
        sin depender de sprites/imágenes externas."""
        if self.recolectado:
            return

        pygame.draw.circle(pantalla, self.color, self._centro(), TAM_CASILLA // 5)


class ItemEscudo(Item):
    """Protege al jugador: la próxima vez que el cazador lo atrape,
    se consume el escudo en vez de perder una vida."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = CELESTE
        self.puntos = 15
        self.tipo="escudo"

    def aplicar_efecto(self, jugador):
        jugador.estadisticas.ganar_escudo()

    def dibujar(self, pantalla):
        if self.recolectado:
            return
        cx, cy = self._centro()
        # Forma de escudo: un pentágono simple
        puntos = [
            (cx - 8, cy - 9), (cx + 8, cy - 9),
            (cx + 8, cy + 3), (cx, cy + 11), (cx - 8, cy + 3),
        ]
        pygame.draw.polygon(pantalla, self.color, puntos)
        pygame.draw.polygon(pantalla, BLANCO, puntos, 1)


class ItemLlave(Item):
    """Se necesita para abrir compuertas (casillas 'D' en el mapa).
    Cada compuerta consume una llave al abrirse."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = AMARILLO
        self.puntos = 20
        self.tipo="llave"

    def aplicar_efecto(self, jugador):
        jugador.estadisticas.ganar_llave()

    def dibujar(self, pantalla):
        if self.recolectado:
            return
        cx, cy = self._centro()
        # Forma de llave: aro (bow) + tallo + dientes
        pygame.draw.circle(pantalla, self.color, (cx - 6, cy), 6, 3)
        pygame.draw.line(pantalla, self.color, (cx, cy), (cx + 11, cy), 3)
        pygame.draw.line(pantalla, self.color, (cx + 11, cy), (cx + 11, cy + 5), 3)
        pygame.draw.line(pantalla, self.color, (cx + 6, cy), (cx + 6, cy + 4), 3)


class ItemVelocidad(Item):
    """Buff temporal: mientras está activo, cada movimiento del
    jugador avanza 2 casillas en vez de 1 (si el camino está libre)."""

    DURACION_MS = 6000

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = VERDE_CLARO
        self.puntos = 25

    def aplicar_efecto(self, jugador):
        jugador.activar_efecto_temporal("velocidad", self.DURACION_MS)

    def dibujar(self, pantalla):
        if self.recolectado:
            return
        cx, cy = self._centro()
        # Ícono "avance rápido": dos chevrones apuntando a la derecha
        pygame.draw.polygon(pantalla, self.color, [(cx - 9, cy - 8), (cx - 9, cy + 8), (cx - 1, cy)])
        pygame.draw.polygon(pantalla, self.color, [(cx - 1, cy - 8), (cx - 1, cy + 8), (cx + 7, cy)])


class ItemLentitud(Item):
    """Perjudicial: mientras está activo, el jugador solo se mueve
    en 1 de cada 2 pulsaciones de tecla (el resto se ignoran)."""

    DURACION_MS = 5000

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = MARRON

    def aplicar_efecto(self, jugador):
        jugador.activar_efecto_temporal("lentitud", self.DURACION_MS)

    def dibujar(self, pantalla):
        if self.recolectado:
            return
        cx, cy = self._centro()
        # Ícono "retroceso": dos chevrones apuntando a la izquierda
        # (espejo del de velocidad, para que se note que es lo opuesto)
        pygame.draw.polygon(pantalla, self.color, [(cx + 9, cy - 8), (cx + 9, cy + 8), (cx + 1, cy)])
        pygame.draw.polygon(pantalla, self.color, [(cx + 1, cy - 8), (cx + 1, cy + 8), (cx - 7, cy)])


class ItemInvertir(Item):
    """Perjudicial: mientras está activo, se invierten los controles
    (arriba<->abajo, izquierda<->derecha)."""

    DURACION_MS = 5000

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = VIOLETA

    def aplicar_efecto(self, jugador):
        jugador.activar_efecto_temporal("invertido", self.DURACION_MS)

    def dibujar(self, pantalla):
        if self.recolectado:
            return
        cx, cy = self._centro()
        # Ícono de "intercambio": una flecha arriba y otra abajo
        pygame.draw.polygon(pantalla, self.color, [(cx - 3, cy + 8), (cx - 8, cy - 1), (cx + 2, cy - 1)])
        pygame.draw.polygon(pantalla, self.color, [(cx + 3, cy - 8), (cx - 2, cy + 1), (cx + 8, cy + 1)])
