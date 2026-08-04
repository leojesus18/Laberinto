import pygame
from constantes import *


class Cazador:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.color = ROJO

        self.contador = 0


    def mover(self, mapa, jugador_x, jugador_y):

        self.contador += 1

        # Se mueve cada 20 frames
        if self.contador < 20:
            return

        self.contador = 0

        nuevo_x = self.x
        nuevo_y = self.y

        # IA simple
        if jugador_x > self.x:
            nuevo_x += 1

        elif jugador_x < self.x:
            nuevo_x -= 1

        elif jugador_y > self.y:
            nuevo_y += 1

        elif jugador_y < self.y:
            nuevo_y -= 1

        # No atravesar paredes
        if mapa[nuevo_y][nuevo_x] != "#":
            self.x = nuevo_x
            self.y = nuevo_y


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


    def atrapo_jugador(self, jugador_x, jugador_y):

        return self.x == jugador_x and self.y == jugador_y