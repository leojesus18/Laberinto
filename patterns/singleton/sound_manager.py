import pygame
import math
import array


class SoundManager:


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

        # Efectos de menú: se generan por código (ondas senoidales) en vez
        # de usar archivos, para no depender de conseguir más .wav/.mp3.
        self._frecuencia_muestreo = 44100
        self.sonido_menu = self._crear_tono(440, 80)
        self.sonido_confirmar = self._crear_tono_doble(523, 659, 90)

    def reproducir_musica(self, ruta, loop=True):
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play(-1 if loop else 0)

    def detener_musica(self):
        pygame.mixer.music.stop()

    def reproducir_sonido(self, sonido):
        sonido.play()

    def reproducir_menu(self):
        self.sonido_menu.play()

    def reproducir_confirmar(self):
        self.sonido_confirmar.play()

    # ---------- Generación de tonos (para los efectos de menú) ----------

    def _crear_tono(self, frecuencia, duracion_ms, volumen=0.4):
        n_muestras = int(self._frecuencia_muestreo * duracion_ms / 1000)
        buffer = array.array("h")
        amplitud = int(32767 * volumen)

        for i in range(n_muestras):
            t = i / self._frecuencia_muestreo
            fade = 1 - (i / n_muestras)
            valor = math.sin(2 * math.pi * frecuencia * t) * fade
            muestra = int(valor * amplitud)
            buffer.append(muestra)
            buffer.append(muestra)

        return pygame.mixer.Sound(buffer=buffer.tobytes())

    def _crear_tono_doble(self, frecuencia1, frecuencia2, duracion_ms, volumen=0.4):
        mitad = duracion_ms // 2
        sonido1 = self._crear_tono(frecuencia1, mitad, volumen)
        sonido2 = self._crear_tono(frecuencia2, mitad, volumen)
        buffer_total = array.array("h")
        buffer_total.frombytes(sonido1.get_raw())
        buffer_total.frombytes(sonido2.get_raw())
        return pygame.mixer.Sound(buffer=buffer_total.tobytes())