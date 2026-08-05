import pygame
import math
import array

from patterns.singleton.configuracion import Configuracion


class GestorSonido:
    """
    Patrón Singleton: una sola instancia genera y reproduce todos los
    efectos de sonido del juego.

    Los sonidos NO son archivos externos (.wav/.mp3): se generan por código
    como ondas senoidales. Así el proyecto no depende de conseguir/incluir
    archivos de audio para tener feedback sonoro.

    Si más adelante quieren música de fondo con un archivo real (mp3/ogg),
    conviene sumarla aparte con pygame.mixer.music, que está pensado para
    pistas largas (a diferencia de pygame.mixer.Sound, pensado para efectos
    cortos como los de acá).
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)

        self.frecuencia_muestreo = 44100

        # Se generan una sola vez al crear el gestor y se reutilizan siempre
        self.sonido_menu = self._crear_tono(440, 80)
        self.sonido_confirmar = self._crear_tono_doble(523, 659, 90)
        self.sonido_atrapado = self._crear_tono_barrido(400, 120, 250)
        self.sonido_victoria = self._crear_arpegio([523, 659, 784, 1047], 110)
        self.sonido_gameover = self._crear_tono_barrido(300, 80, 400)

    # ---------- Generación de tonos ----------

    def _crear_tono(self, frecuencia, duracion_ms, volumen=0.4):
        """Un tono simple (nota) de una frecuencia fija, con fade-out
        al final para evitar el 'click' de audio al cortar el sonido."""

        n_muestras = int(self.frecuencia_muestreo * duracion_ms / 1000)
        buffer = array.array("h")
        amplitud = int(32767 * volumen)

        for i in range(n_muestras):
            t = i / self.frecuencia_muestreo
            fade = 1 - (i / n_muestras)
            valor = math.sin(2 * math.pi * frecuencia * t) * fade
            muestra = int(valor * amplitud)
            buffer.append(muestra)  # canal izquierdo
            buffer.append(muestra)  # canal derecho

        return pygame.mixer.Sound(buffer=buffer.tobytes())

    def _crear_tono_barrido(self, frecuencia_inicial, frecuencia_final, duracion_ms, volumen=0.4):
        """Tono cuya frecuencia cambia progresivamente (efecto 'sirena').
        Útil para sonidos de alerta o de derrota."""

        n_muestras = int(self.frecuencia_muestreo * duracion_ms / 1000)
        buffer = array.array("h")
        amplitud = int(32767 * volumen)
        fase = 0.0

        for i in range(n_muestras):
            progreso = i / n_muestras
            frecuencia_actual = frecuencia_inicial + (frecuencia_final - frecuencia_inicial) * progreso
            fase += frecuencia_actual / self.frecuencia_muestreo
            fade = 1 - progreso
            valor = math.sin(2 * math.pi * fase) * fade
            muestra = int(valor * amplitud)
            buffer.append(muestra)
            buffer.append(muestra)

        return pygame.mixer.Sound(buffer=buffer.tobytes())

    def _crear_tono_doble(self, frecuencia1, frecuencia2, duracion_ms, volumen=0.4):
        """Dos notas seguidas (ej: 'do-mi'), usado para confirmaciones."""

        mitad = duracion_ms // 2
        sonido1 = self._crear_tono(frecuencia1, mitad, volumen)
        sonido2 = self._crear_tono(frecuencia2, mitad, volumen)
        return self._unir_sonidos([sonido1, sonido2])

    def _crear_arpegio(self, frecuencias, duracion_nota_ms, volumen=0.4):
        """Varias notas en secuencia, usado para el jingle de victoria."""

        sonidos = [self._crear_tono(f, duracion_nota_ms, volumen) for f in frecuencias]
        return self._unir_sonidos(sonidos)

    def _unir_sonidos(self, sonidos):
        buffer_total = array.array("h")
        for sonido in sonidos:
            buffer_total.frombytes(sonido.get_raw())
        return pygame.mixer.Sound(buffer=buffer_total.tobytes())

    # ---------- Reproducción ----------

    def _volumen_actual(self):
        return Configuracion().volumen_sonido

    def reproducir_menu(self):
        self.sonido_menu.set_volume(self._volumen_actual())
        self.sonido_menu.play()

    def reproducir_confirmar(self):
        self.sonido_confirmar.set_volume(self._volumen_actual())
        self.sonido_confirmar.play()

    def reproducir_atrapado(self):
        self.sonido_atrapado.set_volume(self._volumen_actual())
        self.sonido_atrapado.play()

    def reproducir_victoria(self):
        self.sonido_victoria.set_volume(self._volumen_actual())
        self.sonido_victoria.play()

    def reproducir_gameover(self):
        self.sonido_gameover.set_volume(self._volumen_actual())
        self.sonido_gameover.play()
