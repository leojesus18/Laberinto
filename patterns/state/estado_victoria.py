import pygame
from patterns.state.estado import Estado
from database.score_repository import ScoreRepository
from patterns.singleton.configuracion import Configuracion
from audio.gestor_sonido import GestorSonido
from constantes import *


class EstadoVictoria(Estado):

    def __init__(self, manejador_estados, tiempo_segundos):
        super().__init__(manejador_estados)
        self.tiempo_segundos = tiempo_segundos
        self.fuente = pygame.font.SysFont(None, 64)
        self.fuente_texto = pygame.font.SysFont(None, 28)

        GestorSonido().reproducir_victoria()
        self._guardar_puntaje()

    def _guardar_puntaje(self):
        config = Configuracion()
        repositorio = ScoreRepository()
        repositorio.guardar_puntaje(
            nombre_jugador="Jugador",
            tiempo_segundos=self.tiempo_segundos,
            dificultad=config.dificultad
        )

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
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 70))

        texto_tiempo = self.fuente_texto.render(
            f"Tiempo: {self.tiempo_segundos:.1f} segundos", True, BLANCO
        )
        pantalla.blit(texto_tiempo, (ANCHO // 2 - texto_tiempo.get_width() // 2, ALTO // 2 - 10))

        texto2 = self.fuente_texto.render("Presioná ENTER para volver al menú", True, BLANCO)
        pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 30))