import pygame

from patterns.state.estado import Estado
from patterns.singleton.configuracion import Configuracion
from audio.gestor_sonido import GestorSonido
from constantes import *


class EstadoDificultad(Estado):

    # (clave interna guardada en Configuracion, texto mostrado en pantalla)
    OPCIONES = [
        ("facil", "Fácil"),
        ("normal", "Normal"),
        ("dificil", "Difícil"),
    ]

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        self.fuente_titulo = pygame.font.SysFont(None, 56)
        self.fuente_opcion = pygame.font.SysFont(None, 40)
        self.fuente_ayuda = pygame.font.SysFont(None, 26)

        # Arranca con el cursor sobre la dificultad actualmente configurada
        config = Configuracion()
        self.indice_seleccionado = 0
        for i, (clave, _) in enumerate(self.OPCIONES):
            if clave == config.dificultad:
                self.indice_seleccionado = i
                break

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP:
                    self.indice_seleccionado = (self.indice_seleccionado - 1) % len(self.OPCIONES)
                    GestorSonido().reproducir_menu()

                elif evento.key == pygame.K_DOWN:
                    self.indice_seleccionado = (self.indice_seleccionado + 1) % len(self.OPCIONES)
                    GestorSonido().reproducir_menu()

                elif evento.key == pygame.K_RETURN:
                    clave, _ = self.OPCIONES[self.indice_seleccionado]
                    Configuracion().dificultad = clave
                    GestorSonido().reproducir_confirmar()

                    from patterns.state.estado_jugando import EstadoJugando
                    self.manejador_estados.cambiar_estado(
                        EstadoJugando(self.manejador_estados)
                    )

                elif evento.key == pygame.K_ESCAPE:
                    from patterns.state.estado_menu import EstadoMenu
                    self.manejador_estados.cambiar_estado(
                        EstadoMenu(self.manejador_estados)
                    )

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        titulo = self.fuente_titulo.render("Elegí la dificultad", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 2 - 140))

        for i, (_, etiqueta) in enumerate(self.OPCIONES):
            seleccionado = (i == self.indice_seleccionado)
            color = VERDE if seleccionado else BLANCO
            texto = f"> {etiqueta} <" if seleccionado else etiqueta

            superficie = self.fuente_opcion.render(texto, True, color)
            pantalla.blit(
                superficie,
                (ANCHO // 2 - superficie.get_width() // 2, ALTO // 2 - 40 + i * 50)
            )

        ayuda = self.fuente_ayuda.render(
            "Flechas para elegir | ENTER confirmar | ESC volver", True, GRIS
        )
        pantalla.blit(ayuda, (ANCHO // 2 - ayuda.get_width() // 2, ALTO // 2 + 140))
