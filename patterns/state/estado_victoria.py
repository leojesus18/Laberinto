import pygame
from patterns.state.estado import Estado
from database.score_repository import ScoreRepository
from patterns.singleton.configuracion import Configuracion
from niveles import NIVELES
from constantes import *



class EstadoVictoria(Estado):

    def __init__(self, manejador_estados, tiempo_segundos, estadisticas, hud, indice_nivel=0):
        super().__init__(manejador_estados)
        self.tiempo_segundos = tiempo_segundos
        self.estadisticas = estadisticas  # se arrastra al nivel siguiente (vidas/escudos/puntaje)
        self.hud = hud
        self.indice_nivel = indice_nivel
        self.hay_siguiente_nivel = (indice_nivel + 1) < len(NIVELES)

        self.fuente = pygame.font.SysFont(None, 64)
        self.fuente_texto = pygame.font.SysFont(None, 28)

        self._guardar_puntaje()

        from patterns.singleton.sound_manager import SoundManager
        sonido = SoundManager()
        sonido.detener_musica()
        sonido.reproducir_sonido(sonido.sonido_victoria)

    def _guardar_puntaje(self):
        config = Configuracion()
        repositorio = ScoreRepository()
        repositorio.guardar_puntaje(
            nombre_jugador=config.nombre_jugador,
            tiempo_segundos=self.tiempo_segundos,
            puntaje=self.estadisticas.puntaje,
            dificultad=config.dificultad
        )

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:

                    if self.hay_siguiente_nivel:
                        from patterns.state.estado_jugando import EstadoJugando
                        self.manejador_estados.cambiar_estado(
                            EstadoJugando(
                                self.manejador_estados,
                                self.indice_nivel + 1,
                                self.estadisticas,
                                self.hud,
                            )
                        )
                    else:
                        from patterns.state.estado_menu import EstadoMenu
                        self.manejador_estados.cambiar_estado(
                            EstadoMenu(self.manejador_estados)
                        )

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        titulo = f"¡NIVEL {self.indice_nivel + 1} SUPERADO!" if self.hay_siguiente_nivel else "¡COMPLETASTE LOS 10 NIVELES!"
        texto = self.fuente.render(titulo, True, VERDE)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 90))

        texto_tiempo = self.fuente_texto.render(
            f"Tiempo del nivel: {self.tiempo_segundos:.1f} segundos", True, BLANCO
        )
        pantalla.blit(texto_tiempo, (ANCHO // 2 - texto_tiempo.get_width() // 2, ALTO // 2 - 30))

        texto_puntaje = self.fuente_texto.render(
            f"Puntaje total: {self.estadisticas.puntaje} puntos", True, AMARILLO
        )
        pantalla.blit(texto_puntaje, (ANCHO // 2 - texto_puntaje.get_width() // 2, ALTO // 2))

        if self.hay_siguiente_nivel:
            texto2 = self.fuente_texto.render(
                f"Presioná ENTER para el nivel {self.indice_nivel + 2}", True, BLANCO
            )
        else:
            texto2 = self.fuente_texto.render("Presioná ENTER para volver al menú", True, BLANCO)

        pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 40))
