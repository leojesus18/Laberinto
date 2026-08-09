import pygame
from patterns.state.estado import Estado
from patterns.singleton.configuracion import Configuracion
from patterns.singleton.sound_manager import SoundManager
from constantes import ANCHO, ALTO


class EstadoDificultad(Estado):
    """Pantalla 3: Dificultad (tarjetas en columna) + resumen de la
    partida al costado."""

    # (clave interna, texto mostrado, descripción, color)
    # (clave, etiqueta, descripción, color, nivel de velocidad del cazador 1-3)
    OPCIONES = [
        ("facil", "FÁCIL", "Un laberinto sencillo y más tiempo para escapar.", (90, 190, 100), 1),
        ("normal", "NORMAL", "Un desafío equilibrado.", (210, 170, 50), 2),
        ("dificil", "DIFÍCIL", "Cazador rápido y letal. Solo para valientes.", (190, 65, 70), 3),
    ]

    NOMBRES_PERSONAJE = {
        "estudiante_chico": "Estudiante",
        "estudiante_chica": "Estudiante",
        "profesor": "Profesor",
        "profesora": "Profesora",
    }

    PANEL_OSCURO = (20, 26, 40)
    PANEL_CLARO = (30, 38, 56)
    BORDE_PANEL = (90, 100, 130)
    AMARILLO_FOCO = (255, 210, 90)
    CELESTE_TITULO = (90, 220, 230)
    VERDE_SELECCION = (60, 140, 70)
    VERDE_BORDE = (140, 220, 130)
    ROJO_BOTON = (120, 40, 48)
    ROJO_BORDE = (210, 90, 95)

    ANCHO_TARJETA = 200
    ESPACIO_TARJETA = 15
    ALTO_TARJETA = 200
    ALTO_RESUMEN = 280
    Y_TARJETAS = 177
    X_INICIO = 20

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        self.fuente_titulo = pygame.font.SysFont("arial", 32, bold=True)
        self.fuente_opcion = pygame.font.SysFont("arial", 22, bold=True)
        self.fuente_desc = pygame.font.SysFont("arial", 16)
        self.fuente_resumen_titulo = pygame.font.SysFont("arial", 17, bold=True)
        self.fuente_resumen_etiqueta = pygame.font.SysFont("arial", 14)
        self.fuente_resumen_valor = pygame.font.SysFont("arial", 18, bold=True)
        self.fuente_boton = pygame.font.SysFont("arial", 22, bold=True)
        self.fuente_ayuda = pygame.font.SysFont("arial", 17)

        imagen_original = pygame.image.load("assets/images/fondo_dificultad.png").convert()
        self.fondo = pygame.transform.smoothscale(imagen_original, (ANCHO, ALTO))

        config = Configuracion()
        self.indice_seleccionado = 0
        for i, (clave, *_resto) in enumerate(self.OPCIONES):
            if clave == config.dificultad:
                self.indice_seleccionado = i
                break

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_UP, pygame.K_LEFT):
                    self.indice_seleccionado = (self.indice_seleccionado - 1) % len(self.OPCIONES)
                    SoundManager().reproducir_menu()

                elif evento.key in (pygame.K_DOWN, pygame.K_RIGHT):
                    self.indice_seleccionado = (self.indice_seleccionado + 1) % len(self.OPCIONES)
                    SoundManager().reproducir_menu()

                elif evento.key == pygame.K_RETURN:
                    clave, *_resto = self.OPCIONES[self.indice_seleccionado]
                    Configuracion().dificultad = clave
                    SoundManager().reproducir_confirmar()
                    from patterns.state.estado_jugando import EstadoJugando
                    self.manejador_estados.cambiar_estado(
                        EstadoJugando(self.manejador_estados)
                    )

                elif evento.key == pygame.K_ESCAPE:
                    from patterns.state.estado_nombre import EstadoNombre
                    self.manejador_estados.cambiar_estado(
                        EstadoNombre(self.manejador_estados)
                    )

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))

        titulo = self.fuente_titulo.render("ELEGÍ LA DIFICULTAD", True, self.AMARILLO_FOCO)
        cartel_titulo = pygame.Rect(0, 0, titulo.get_width() + 50, titulo.get_height() + 24)
        cartel_titulo.center = (ANCHO // 2, 107 + titulo.get_height() // 2)
        pygame.draw.rect(pantalla, self.PANEL_OSCURO, cartel_titulo, border_radius=10)
        pygame.draw.rect(pantalla, self.BORDE_PANEL, cartel_titulo, width=3, border_radius=10)
        pantalla.blit(titulo, (cartel_titulo.centerx - titulo.get_width() // 2,
                                cartel_titulo.centery - titulo.get_height() // 2))
        
        ancho_tarjetas = 3 * self.ANCHO_TARJETA + 2 * self.ESPACIO_TARJETA
        x_resumen = self.X_INICIO + ancho_tarjetas + 20
        ancho_resumen = ANCHO - x_resumen - self.X_INICIO

        self._dibujar_tarjetas(pantalla)
        self._dibujar_resumen(pantalla, x_resumen, ancho_resumen)

        y_botones = self.Y_TARJETAS + max(self.ALTO_TARJETA, self.ALTO_RESUMEN) + 25
        ancho_total = x_resumen + ancho_resumen - self.X_INICIO
        self._dibujar_botones(pantalla, y_botones, ancho_total)

        ayuda = self.fuente_ayuda.render(
            "← → ↑ ↓ elegir dificultad", True, (190, 190, 190)
        )
        pantalla.blit(ayuda, (ANCHO // 2 - ayuda.get_width() // 2, ALTO - 40))

    def _dibujar_tarjetas(self, pantalla):
        for i, (_clave, etiqueta, descripcion, color, nivel_velocidad) in enumerate(self.OPCIONES):
            x = self.X_INICIO + i * (self.ANCHO_TARJETA + self.ESPACIO_TARJETA)
            rect = pygame.Rect(x, self.Y_TARJETAS, self.ANCHO_TARJETA, self.ALTO_TARJETA)

            seleccionada = (i == self.indice_seleccionado)
            fondo = self.PANEL_CLARO if seleccionada else self.PANEL_OSCURO
            grosor = 5 if seleccionada else 2

            pygame.draw.rect(pantalla, fondo, rect, border_radius=10)
            pygame.draw.rect(pantalla, color, rect, width=grosor, border_radius=10)

            # Cabecera de color con el círculo + etiqueta
            cabecera = pygame.Rect(rect.x, rect.y, rect.width, 45)
            pygame.draw.rect(pantalla, color, cabecera,
                              border_top_left_radius=8, border_top_right_radius=8)
            pygame.draw.circle(pantalla, (255, 255, 255), (rect.x + 25, rect.y + 22), 8)
            texto_etiqueta = self.fuente_opcion.render(etiqueta, True, (255, 255, 255))
            pantalla.blit(texto_etiqueta, (rect.x + 42, rect.y + 12))

            # Descripción, con salto de línea simple por palabras
            self._dibujar_texto_multilinea(pantalla, descripcion, self.fuente_desc,
                                            (230, 230, 230), rect.x + 15, rect.y + 65,
                                            rect.width - 30)

            # Medidor de velocidad del cazador (llena el espacio vacío
            # y suma información útil sobre qué cambia en cada dificultad)
            etiqueta_vel = self.fuente_resumen_etiqueta.render("VELOCIDAD DEL CAZADOR", True, (170, 170, 180))
            pantalla.blit(etiqueta_vel, (rect.x + 15, rect.y + 140))

            for nivel in range(1, 4):
                cuadro = pygame.Rect(rect.x + 15 + (nivel - 1) * 30, rect.y + 162, 24, 24)
                if nivel <= nivel_velocidad:
                    pygame.draw.rect(pantalla, color, cuadro, border_radius=4)
                else:
                    pygame.draw.rect(pantalla, (60, 65, 80), cuadro, border_radius=4)
                pygame.draw.rect(pantalla, (255, 255, 255), cuadro, width=1, border_radius=4)

    def _dibujar_texto_multilinea(self, pantalla, texto, fuente, color, x, y, ancho_maximo):
        palabras = texto.split(" ")
        linea = ""
        for palabra in palabras:
            prueba = (linea + " " + palabra).strip()
            if fuente.size(prueba)[0] > ancho_maximo and linea:
                render = fuente.render(linea, True, color)
                pantalla.blit(render, (x, y))
                y += 22
                linea = palabra
            else:
                linea = prueba
        if linea:
            render = fuente.render(linea, True, color)
            pantalla.blit(render, (x, y))

    def _dibujar_resumen(self, pantalla, x, ancho):
        config = Configuracion()
        dificultad_actual = self.OPCIONES[self.indice_seleccionado][1]
        personaje = self.NOMBRES_PERSONAJE.get(config.personaje_jugador, "Estudiante")

        rect = pygame.Rect(x, self.Y_TARJETAS, ancho, self.ALTO_RESUMEN)
        pygame.draw.rect(pantalla, self.PANEL_OSCURO, rect, border_radius=10)
        pygame.draw.rect(pantalla, self.BORDE_PANEL, rect, width=2, border_radius=10)

        titulo = self.fuente_resumen_titulo.render("RESUMEN DE LA PARTIDA", True, self.CELESTE_TITULO)
        pantalla.blit(titulo, (rect.x + 15, rect.y + 15))
        pygame.draw.line(pantalla, self.BORDE_PANEL,
                          (rect.x + 15, rect.y + 38), (rect.right - 15, rect.y + 38), 1)

        filas = [
            ("MODO", "1 JUGADOR"),
            ("JUGADOR", config.nombre_jugador or "Jugador"),
            ("PERSONAJE", personaje),
            ("DIFICULTAD", dificultad_actual),
        ]

        fila_y = rect.y + 55
        for etiqueta, valor in filas:
            texto_etiqueta = self.fuente_resumen_etiqueta.render(etiqueta + ":", True, (160, 160, 170))
            pantalla.blit(texto_etiqueta, (rect.x + 15, fila_y))
            texto_valor = self.fuente_resumen_valor.render(valor, True, (255, 255, 255))
            pantalla.blit(texto_valor, (rect.x + 15, fila_y + 18))
            fila_y += 55

    def _dibujar_botones(self, pantalla, y, ancho_total):
        ancho_boton = (ancho_total - 20) // 2

        rect_comenzar = pygame.Rect(self.X_INICIO, y, ancho_boton, 50)
        pygame.draw.rect(pantalla, self.VERDE_SELECCION, rect_comenzar, border_radius=6)
        pygame.draw.rect(pantalla, self.VERDE_BORDE, rect_comenzar, width=3, border_radius=6)
        texto_comenzar = self.fuente_boton.render("COMENZAR (ENTER)", True, (255, 255, 255))
        pantalla.blit(texto_comenzar, (rect_comenzar.centerx - texto_comenzar.get_width() // 2,
                                        rect_comenzar.centery - texto_comenzar.get_height() // 2))

        rect_volver = pygame.Rect(rect_comenzar.right + 20, y, ancho_boton, 50)
        pygame.draw.rect(pantalla, self.ROJO_BOTON, rect_volver, border_radius=6)
        pygame.draw.rect(pantalla, self.ROJO_BORDE, rect_volver, width=3, border_radius=6)
        texto_volver = self.fuente_boton.render("VOLVER (ESC)", True, (255, 255, 255))
        pantalla.blit(texto_volver, (rect_volver.centerx - texto_volver.get_width() // 2,
                                      rect_volver.centery - texto_volver.get_height() // 2))