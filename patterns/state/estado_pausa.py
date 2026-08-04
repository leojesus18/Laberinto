import pygame
from patterns.state.estado import Estado
from constantes import *


class EstadoPausa(Estado):

    def __init__(self, manejador_estados, estado_jugando):
        super().__init__(manejador_estados)
        # Guardamos el estado "Jugando" para poder volver a él tal cual estaba
        self.estado_jugando = estado_jugando
        self.fuente = pygame.font.SysFont(None, 56)
        self.fuente_texto = pygame.font.SysFont(None, 28)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.manejador_estados.cambiar_estado(self.estado_jugando)

                elif evento.key == pygame.K_m:
                    from patterns.state.estado_menu import EstadoMenu
                    self.manejador_estados.cambiar_estado(
                        EstadoMenu(self.manejador_estados)
                    )

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        # Dibuja el juego "congelado" de fondo
        self.estado_jugando.dibujar(pantalla)

        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(180)
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0, 0))

        texto = self.fuente.render("PAUSA", True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))

        texto2 = self.fuente_texto.render("ESC para continuar | M para menú", True, BLANCO)
        pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 10))