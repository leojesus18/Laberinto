import sys
import pygame
from patterns.state.estado import Estado
from constantes import ANCHO, ALTO


class EstadoMenu(Estado):
   #Pantalla 1: Menú Principal

    OPCIONES = ["Nueva Partida", "Cómo Jugar", "Salir"]

    # Colores tomados de la paleta del mockup (facultad / pixel art)
    VERDE_SELECCION = (60, 140, 70)
    VERDE_BORDE = (140, 220, 130)
    PANEL_OSCURO = (20, 26, 40)
    BORDE_PANEL = (90, 100, 130)
    NARANJA_TITULO = (255, 170, 30)
    CELESTE_SUBTITULO = (90, 220, 230)

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)

        imagen_original = pygame.image.load("assets/images/fondo_menu.png").convert()
        self.fondo = pygame.transform.smoothscale(imagen_original, (ANCHO, ALTO))

        self.fuente_titulo = pygame.font.SysFont("arial", 46, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("arial", 22, bold=True)
        self.fuente_opcion = pygame.font.SysFont("arial", 28, bold=True)
        self.fuente_ayuda = pygame.font.SysFont("arial", 22)

        self.opcion_seleccionada = 0
        self.mostrando_ayuda = False

        # Al entrar al menú desde cualquier lado (portada, pausa, game
        # over, etc.) nos aseguramos de que suene la música de menú,
        # aunque en ese momento estuviera sonando la del laberinto.
        from patterns.singleton.sound_manager import SoundManager
        sonido = SoundManager()
        sonido.reproducir_musica(sonido.musica_menu)

    def manejar_eventos(self, eventos):
        from patterns.singleton.sound_manager import SoundManager
        sonido = SoundManager()

        for evento in eventos:
            if evento.type != pygame.KEYDOWN:
                continue

            if self.mostrando_ayuda:
                # Estando en el cartel de ayuda, cualquier tecla vuelve al menú
                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.mostrando_ayuda = False
                continue

            if evento.key == pygame.K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.OPCIONES)
                sonido.reproducir_menu()
            elif evento.key == pygame.K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.OPCIONES)
                sonido.reproducir_menu()
            elif evento.key == pygame.K_RETURN:
                sonido.reproducir_confirmar()
                self._confirmar_opcion()

    def _confirmar_opcion(self):
        opcion = self.OPCIONES[self.opcion_seleccionada]

        if opcion == "Nueva Partida":
            from patterns.state.estado_nombre import EstadoNombre
            self.manejador_estados.cambiar_estado(
                EstadoNombre(self.manejador_estados)
            )
        elif opcion == "Cómo Jugar":
            self.mostrando_ayuda = True
        elif opcion == "Salir":
            pygame.quit()
            sys.exit()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))

        if self.mostrando_ayuda:
            self._dibujar_ayuda(pantalla)
        else:
            self._dibujar_opciones(pantalla)

    def _dibujar_titulo(self, pantalla):
        self._texto_con_sombra(pantalla, "EL LABERINTO", self.fuente_titulo,
                                self.NARANJA_TITULO, ANCHO // 2, 90)
        self._texto_con_sombra(pantalla, "ESCAPE DE LA FACU", self.fuente_subtitulo,
                                self.CELESTE_SUBTITULO, ANCHO // 2, 130)

    def _texto_con_sombra(self, pantalla, texto, fuente, color, centro_x, y):
        sombra = fuente.render(texto, True, (0, 0, 0))
        pantalla.blit(sombra, (centro_x - sombra.get_width() // 2 + 3, y + 3))
        render = fuente.render(texto, True, color)
        pantalla.blit(render, (centro_x - render.get_width() // 2, y))

    def _dibujar_opciones(self, pantalla):
        ancho_boton, alto_boton = 320, 55
        espacio = 15
        x = ANCHO // 2 - ancho_boton // 2
        y_inicial = 220

        for i, opcion in enumerate(self.OPCIONES):
            y = y_inicial + i * (alto_boton + espacio)
            rect = pygame.Rect(x, y, ancho_boton, alto_boton)

            seleccionado = (i == self.opcion_seleccionada)
            color_fondo = self.VERDE_SELECCION if seleccionado else self.PANEL_OSCURO
            color_borde = self.VERDE_BORDE if seleccionado else self.BORDE_PANEL

            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=6)
            pygame.draw.rect(pantalla, color_borde, rect, width=3, border_radius=6)

            texto = self.fuente_opcion.render(opcion, True, (255, 255, 255))
            pantalla.blit(texto, (rect.centerx - texto.get_width() // 2,
                                   rect.centery - texto.get_height() // 2))

    def _dibujar_ayuda(self, pantalla):
        panel = pygame.Rect(ANCHO // 2 - 260, 190, 520, 260)
        pygame.draw.rect(pantalla, self.PANEL_OSCURO, panel, border_radius=8)
        pygame.draw.rect(pantalla, self.BORDE_PANEL, panel, width=3, border_radius=8)

        lineas = [
            "Movete con las flechas del teclado.",
            "Escapá del laberinto antes de que",
            "te atrape el cazador.",
            "",
            "Recolectá llaves para abrir compuertas",
            "y escudos para protegerte de un golpe.",
            "",
            "Presioná ENTER para volver",
        ]

        y = panel.y + 25
        for linea in lineas:
            texto = self.fuente_ayuda.render(linea, True, (230, 230, 230))
            pantalla.blit(texto, (panel.centerx - texto.get_width() // 2, y))
            y += 30