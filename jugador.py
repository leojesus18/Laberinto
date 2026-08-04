import pygame
from constantes import *


class Jugador:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = AZUL

    def mover(self, mapa, dx, dy):
        """Intenta mover al jugador dx, dy casillas. Respeta paredes y bordes del mapa."""
        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        # Evita salir del mapa
        if 0 <= nuevo_y < len(mapa) and 0 <= nuevo_x < len(mapa[0]):
            # Evita atravesar paredes
            if mapa[nuevo_y][nuevo_x] != "#":
                self.x = nuevo_x
                self.y = nuevo_y

    def llego_a_salida(self, mapa):
        return mapa[self.y][self.x] == "S"

    def dibujar(self, pantalla):
        pygame.draw.circle(
            pantalla,
            self.color,
            (
                self.x * TAM_CASILLA + TAM_CASILLA // 2,
                self.y * TAM_CASILLA + TAM_CASILLA // 2
            ),
            TAM_CASILLA // 3
        )