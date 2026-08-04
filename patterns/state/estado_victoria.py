import pygame
from patterns.state.estado import Estado
from constantes import *


class EstadoVictoria(Estado):

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        self.fuente = pygame.font.SysFont(None, 64)
        self.fuente_texto = pygame.font.SysFont(None, 28)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    from patterns.state.estado_menu import EstadoMenu
                    self.manejador_estados.cambiar_estado(
                        EstadoMenu(self.manejador_estados)
                    )

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        texto = self.fuente.render("¡GANASTE!", True, VERDE)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))

        texto2 = self.fuente_texto.render("Presioná ENTER para volver al menú", True, BLANCO)
        pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 20))