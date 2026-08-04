import pygame
from patterns.state.estado import Estado
from jugador import Jugador
from cazador import Cazador
from constantes import *
from niveles import nivel1


class EstadoJugando(Estado):

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        self.mapa = [fila[:] for fila in nivel1]

        jugador_x, jugador_y, cazador_x, cazador_y = self._buscar_posiciones_iniciales()

        self.jugador = Jugador(jugador_x, jugador_y)
        self.cazador = Cazador(cazador_x, cazador_y)

    def _buscar_posiciones_iniciales(self):
        jugador_x = jugador_y = 0
        cazador_x = cazador_y = 0

        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):
                if self.mapa[fila][columna] == "P":
                    jugador_x, jugador_y = columna, fila
                elif self.mapa[fila][columna] == "C":
                    cazador_x, cazador_y = columna, fila

        return jugador_x, jugador_y, cazador_x, cazador_y

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    from patterns.state.estado_pausa import EstadoPausa
                    self.manejador_estados.cambiar_estado(
                        EstadoPausa(self.manejador_estados, self)
                    )
                    return

                dx = dy = 0
                if evento.key == pygame.K_UP:
                    dy = -1
                elif evento.key == pygame.K_DOWN:
                    dy = 1
                elif evento.key == pygame.K_LEFT:
                    dx = -1
                elif evento.key == pygame.K_RIGHT:
                    dx = 1

                if dx != 0 or dy != 0:
                    self.jugador.mover(self.mapa, dx, dy)

                    if self.jugador.llego_a_salida(self.mapa):
                        from patterns.state.estado_victoria import EstadoVictoria
                        self.manejador_estados.cambiar_estado(
                            EstadoVictoria(self.manejador_estados)
                        )

    def actualizar(self):
        self.cazador.mover(self.mapa, self.jugador.x, self.jugador.y)

        if self.cazador.atrapo_jugador(self.jugador.x, self.jugador.y):
            from patterns.state.estado_gameover import EstadoGameOver
            self.manejador_estados.cambiar_estado(
                EstadoGameOver(self.manejador_estados)
            )

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):
                caracter = self.mapa[fila][columna]

                rect = pygame.Rect(
                    columna * TAM_CASILLA,
                    fila * TAM_CASILLA,
                    TAM_CASILLA,
                    TAM_CASILLA
                )

                if caracter == "#":
                    pygame.draw.rect(pantalla, GRIS, rect)
                elif caracter == "S":
                    pygame.draw.rect(pantalla, VERDE, rect)
                else:
                    pygame.draw.rect(pantalla, BLANCO, rect)

        self.jugador.dibujar(pantalla)
        self.cazador.dibujar(pantalla)