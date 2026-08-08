import pygame
from patterns.state.estado import Estado
from constantes import *


class EstadoMenu(Estado):

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        self.fuente_titulo = pygame.font.SysFont(None, 64)
        self.fuente_texto = pygame.font.SysFont(None, 32)

        from patterns.singleton.sound_manager import SoundManager
        sonido = SoundManager()
        sonido.reproducir_musica(sonido.musica_menu)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    from patterns.singleton.sound_manager import SoundManager
                    SoundManager().reproducir_confirmar()

                    # Import acá adentro para evitar import circular
                    from patterns.state.estado_dificultad import EstadoDificultad
                    self.manejador_estados.cambiar_estado(
                        EstadoDificultad(self.manejador_estados)
                    )

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        titulo = self.fuente_titulo.render("Escape del Laberinto", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 2 - 80))

        texto = self.fuente_texto.render("Presioná ENTER para jugar", True, VERDE)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + 10))