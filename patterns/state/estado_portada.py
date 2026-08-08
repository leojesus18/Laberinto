import pygame
from patterns.state.estado import Estado
from constantes import ANCHO, ALTO


class EstadoPortada(Estado):
    
   #Pantalla de portada/título: la primera que ve el jugador al abrirel juego.

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)

        imagen_original = pygame.image.load("assets/images/portada.png").convert()
        self.fondo = pygame.transform.smoothscale(imagen_original, (ANCHO, ALTO))

        from patterns.singleton.sound_manager import SoundManager
        SoundManager().reproducir_musica(SoundManager().musica_menu)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                from patterns.singleton.sound_manager import SoundManager
                SoundManager().reproducir_confirmar()

                from patterns.state.estado_menu import EstadoMenu
                self.manejador_estados.cambiar_estado(
                    EstadoMenu(self.manejador_estados)
                )

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))