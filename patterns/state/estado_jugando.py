import pygame
from patterns.state.estado import Estado
from jugador import Jugador
from cazador import Cazador
from constantes import *
from niveles import nivel1
from patterns.factory.item_factory import generar_items_desde_mapa


class EstadoJugando(Estado):

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        # list(nivel1) copia la lista de filas: así, si el jugador abre
        # una compuerta, se modifica esta copia y no el mapa original de
        # niveles.py (que se reutilizaría "roto" en la próxima partida).
        self.mapa = list(nivel1)

        jugador_x, jugador_y, cazador_x, cazador_y = self._buscar_posiciones_iniciales()

        self.jugador = Jugador(jugador_x, jugador_y)
        self.cazador = Cazador(cazador_x, cazador_y)
        self.items = generar_items_desde_mapa(self.mapa)
        self.tiempo_inicio=pygame.time.get_ticks()
        self.vidas=3

        from patterns.singleton.sound_manager import SoundManager
        self.sonido = SoundManager()
        self.sonido.reproducir_musica(self.sonido.musica_juego)

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
                    self.sonido.reproducir_sonido(self.sonido.sonido_movimiento_jugador)
                    self._recolectar_item_si_corresponde()

                    if self.jugador.llego_a_salida(self.mapa):
                        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) / 1000

                        from patterns.state.estado_victoria import EstadoVictoria
                        self.manejador_estados.cambiar_estado(
                            EstadoVictoria(self.manejador_estados, tiempo_transcurrido)
                        )

    def _recolectar_item_si_corresponde(self):
        for item in self.items:
            if item.recolectado:
                continue

            if item.x == self.jugador.x and item.y == self.jugador.y:
                item.aplicar_efecto(self.jugador)
                item.recolectado = True
                self.sonido.reproducir_sonido(self.sonido.sonido_movimiento_jugador)

    def actualizar(self):
        self.cazador.mover(self.mapa, self.jugador.x, self.jugador.y)

        if self.cazador.atrapo_jugador(self.jugador.x, self.jugador.y):
            self.sonido.reproducir_sonido(self.sonido.sonido_movimiento_cazador)

            pierde_vida = self.jugador.recibir_golpe()  # False si un escudo absorbió el golpe

            if pierde_vida:
                self.vidas -= 1

            if self.vidas <= 0:
                from patterns.state.estado_gameover import EstadoGameOver
                self.manejador_estados.cambiar_estado(
                    EstadoGameOver(self.manejador_estados)
                )
            else:
                jugador_x, jugador_y, cazador_x, cazador_y = self._buscar_posiciones_iniciales()
                self.jugador.x = jugador_x
                self.jugador.y = jugador_y
                self.cazador.x = cazador_x
                self.cazador.y = cazador_y

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
                elif caracter == "D":
                    pygame.draw.rect(pantalla, MARRON_OSCURO, rect)
                else:
                    pygame.draw.rect(pantalla, BLANCO, rect)

        for item in self.items:
            item.dibujar(pantalla)

        self.jugador.dibujar(pantalla)
        self.cazador.dibujar(pantalla)
        fuente_hud = pygame.font.SysFont(None, 28)
        texto_hud = fuente_hud.render(
            f"Vidas: {self.vidas}   Escudos: {self.jugador.escudos}   Llaves: {self.jugador.llaves}",
            True, BLANCO
        )
        pantalla.blit(texto_hud, (10, 10))