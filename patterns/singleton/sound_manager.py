import pygame


class SoundManager:
    """
    Patrón Singleton aplicado al manejo de audio.
    Una sola instancia controla toda la música y los efectos de sonido
    del juego, evitando conflictos si distintas partes del código
    intentaran reproducir audio por separado.
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.sonido_movimiento_jugador = pygame.mixer.Sound("assets/sounds/movimiento1.wav")
        self.sonido_movimiento_cazador = pygame.mixer.Sound("assets/sounds/movimiento2.wav")
        self.sonido_victoria = pygame.mixer.Sound("assets/sounds/victoria.mp3")
        self.sonido_gameover = pygame.mixer.Sound("assets/sounds/gameover.mp3")

        self.musica_menu = "assets/sounds/instrumental2.mp3"
        self.musica_juego = "assets/sounds/instrumental1.mp3"

    def reproducir_musica(self, ruta, loop=True):
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play(-1 if loop else 0)

    def detener_musica(self):
        pygame.mixer.music.stop()

    def reproducir_sonido(self, sonido):
        sonido.play()