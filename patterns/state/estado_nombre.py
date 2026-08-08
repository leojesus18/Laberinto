import pygame
from patterns.state.estado import Estado
from patterns.singleton.configuracion import Configuracion
from constantes import *


class EstadoNombre(Estado):
    """
    Pantalla donde el jugador escribe su nombre antes de jugar.
    El nombre se guarda en Configuracion (Singleton) para que el resto
    del juego lo use al guardar puntajes e ítems en MySQL, en vez del
    nombre fijo "Jugador" que se usaba antes.
    """

    MAX_CARACTERES = 15

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        self.fuente_titulo = pygame.font.SysFont(None, 56)
        self.fuente_texto = pygame.font.SysFont(None, 40)
        self.fuente_ayuda = pygame.font.SysFont(None, 26)

        # Si ya había un nombre cargado antes, arrancar con ese
        self.texto = Configuracion().nombre_jugador or ""

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    nombre = self.texto.strip()
                    if nombre == "":
                        nombre = "Jugador"

                    Configuracion().nombre_jugador = nombre

                    from patterns.singleton.sound_manager import SoundManager
                    SoundManager().reproducir_confirmar()

                    from patterns.state.estado_dificultad import EstadoDificultad
                    self.manejador_estados.cambiar_estado(
                        EstadoDificultad(self.manejador_estados)
                    )

                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]

                elif evento.key == pygame.K_ESCAPE:
                    from patterns.state.estado_menu import EstadoMenu
                    self.manejador_estados.cambiar_estado(
                        EstadoMenu(self.manejador_estados)
                    )

                else:
                    caracter = evento.unicode
                    if caracter.isprintable() and len(self.texto) < self.MAX_CARACTERES:
                        self.texto += caracter

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        titulo = self.fuente_titulo.render("¿Cómo te llamás?", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 2 - 100))

        # Caja de texto con el nombre que se va escribiendo
        caja = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 - 20, 300, 45)
        pygame.draw.rect(pantalla, GRIS, caja, 2)

        texto_render = self.fuente_texto.render(self.texto, True, VERDE)
        pantalla.blit(texto_render, (caja.x + 10, caja.y + 8))

        ayuda = self.fuente_ayuda.render(
            "Escribí tu nombre | ENTER confirmar | ESC volver", True, GRIS
        )
        pantalla.blit(ayuda, (ANCHO // 2 - ayuda.get_width() // 2, ALTO // 2 + 80))