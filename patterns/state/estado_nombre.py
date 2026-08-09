import pygame
from patterns.state.estado import Estado
from patterns.singleton.configuracion import Configuracion
from constantes import ANCHO, ALTO


class EstadoNombre(Estado):
   #Pantalla 2: Configurar Partida. Modo de juego, nombre del jugador, y selección de personaje/cazador.
   #TAB cambia el "campo" activo

    MAX_CARACTERES = 15
    CAMPOS = ["nombre", "personaje", "cazador"]

    PERSONAJES = [
        ("estudiante_chico", "assets/images/personajes/estudiante_chico.png"),
        ("estudiante_chica", "assets/images/personajes/estudiante_chica.png"),
        ("profesor", "assets/images/personajes/profesor.png"),
        ("profesora", "assets/images/personajes/profesora.png"),
    ]

    CAZADORES = [
        ("cazador", "assets/images/personajes/cazador.png"),
        ("cazadora", "assets/images/personajes/cazadora.png"),
    ]

    VERDE_SELECCION = (60, 140, 70)
    VERDE_BORDE = (140, 220, 130)
    ROJO_BOTON = (120, 40, 48)
    ROJO_BORDE = (210, 90, 95)
    PANEL_OSCURO = (20, 26, 40)
    BORDE_PANEL = (90, 100, 130)
    AMARILLO_FOCO = (255, 210, 90)
    BLANCO_TITULO = (220, 220, 220)
    GRIS_TEXTO = (150, 150, 150)

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)

        imagen_original = pygame.image.load("assets/images/fondo_configurar.png").convert()
        self.fondo = pygame.transform.smoothscale(imagen_original, (ANCHO, ALTO))

        self.fuente_seccion = pygame.font.SysFont("arial", 20, bold=True)
        self.fuente_texto = pygame.font.SysFont("arial", 24, bold=True)
        self.fuente_chica = pygame.font.SysFont("arial", 15)
        self.fuente_ayuda = pygame.font.SysFont("arial", 17)
        self.fuente_boton = pygame.font.SysFont("arial", 22, bold=True)

        self.texto = Configuracion().nombre_jugador or ""

        self.indice_campo = 0  # 0=nombre, 1=personaje, 2=cazador
        self.indice_personaje = 0
        self.indice_cazador = 0

        self.miniaturas = [self._cargar_miniatura(r, 120) for _c, r in self.PERSONAJES]
        self.miniaturas_cazador = [self._cargar_miniatura(r, 120) for _c, r in self.CAZADORES]
        
    def _cargar_miniatura(self, ruta, tamano):
        imagen = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.smoothscale(imagen, (tamano, tamano))

    def manejar_eventos(self, eventos):
        from patterns.singleton.sound_manager import SoundManager
        sonido = SoundManager()
        campo_actual = self.CAMPOS[self.indice_campo]

        for evento in eventos:
            if evento.type != pygame.KEYDOWN:
                continue

            if evento.key == pygame.K_RETURN:
                config = Configuracion()
                config.nombre_jugador = self.texto.strip() or "Jugador"
                config.personaje_jugador = self.PERSONAJES[self.indice_personaje][0]
                config.personaje_cazador = self.CAZADORES[self.indice_cazador][0]

                sonido.reproducir_confirmar()

                from patterns.state.estado_dificultad import EstadoDificultad
                self.manejador_estados.cambiar_estado(
                    EstadoDificultad(self.manejador_estados)
                )

            elif evento.key == pygame.K_ESCAPE:
                from patterns.state.estado_menu import EstadoMenu
                self.manejador_estados.cambiar_estado(
                    EstadoMenu(self.manejador_estados)
                )

            elif evento.key == pygame.K_TAB:
                self.indice_campo = (self.indice_campo + 1) % len(self.CAMPOS)
                sonido.reproducir_menu()

            elif evento.key == pygame.K_LEFT:
                if campo_actual == "personaje":
                    self.indice_personaje = (self.indice_personaje - 1) % len(self.PERSONAJES)
                    sonido.reproducir_menu()
                elif campo_actual == "cazador":
                    self.indice_cazador = (self.indice_cazador - 1) % len(self.CAZADORES)
                    sonido.reproducir_menu()

            elif evento.key == pygame.K_RIGHT:
                if campo_actual == "personaje":
                    self.indice_personaje = (self.indice_personaje + 1) % len(self.PERSONAJES)
                    sonido.reproducir_menu()
                elif campo_actual == "cazador":
                    self.indice_cazador = (self.indice_cazador + 1) % len(self.CAZADORES)
                    sonido.reproducir_menu()

            elif campo_actual == "nombre" and evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]

            elif campo_actual == "nombre":
                caracter = evento.unicode
                if caracter.isprintable() and len(self.texto) < self.MAX_CARACTERES:
                    self.texto += caracter

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))

        panel = pygame.Rect(ANCHO // 2 - 300, 12, 600, ALTO - 24)
        pygame.draw.rect(pantalla, self.PANEL_OSCURO, panel, border_radius=10)
        pygame.draw.rect(pantalla, self.BORDE_PANEL, panel, width=3, border_radius=10)

        campo_actual = self.CAMPOS[self.indice_campo]

        y = panel.y + 14
        y = self._dibujar_modo_juego(pantalla, panel, y)
        y = self._dibujar_nombre(pantalla, panel, y, foco=(campo_actual == "nombre"))
        y = self._dibujar_fila_personajes(pantalla, panel, y, "3. TU PERSONAJE",
                                           self.miniaturas, self.indice_personaje,
                                           foco=(campo_actual == "personaje"))
        y = self._dibujar_fila_personajes(pantalla, panel, y, "4. TU CAZADOR",
                                           self.miniaturas_cazador, self.indice_cazador,
                                           foco=(campo_actual == "cazador"))

        self._dibujar_botones(pantalla, panel, y)

        ayuda = self.fuente_ayuda.render(
            "TAB cambiar campo | ← → elegir", True, (190, 190, 190)
        )
        pantalla.blit(ayuda, (panel.centerx - ayuda.get_width() // 2, panel.bottom - 22))

    def _titulo_seccion(self, pantalla, panel, y, texto, foco):
        x_texto = panel.x + 20

        if foco:
            # Triangulito de foco (dibujado, no depende de que la fuente
            # tenga el glifo de una flecha - por eso antes se veía "roto")
            puntas = [(panel.x + 20, y + 6), (panel.x + 20, y + 18), (panel.x + 30, y + 12)]
            pygame.draw.polygon(pantalla, self.AMARILLO_FOCO, puntas)
            x_texto = panel.x + 38

        color = self.AMARILLO_FOCO if foco else self.BLANCO_TITULO
        render = self.fuente_seccion.render(texto, True, color)
        pantalla.blit(render, (x_texto, y))
        return y + 30

    def _dibujar_modo_juego(self, pantalla, panel, y):
        y = self._titulo_seccion(pantalla, panel, y, "1. MODO DE JUEGO", foco=False)

        rect_1j = pygame.Rect(panel.x + 20, y, 200, 40)
        pygame.draw.rect(pantalla, self.VERDE_SELECCION, rect_1j, border_radius=6)
        pygame.draw.rect(pantalla, self.VERDE_BORDE, rect_1j, width=3, border_radius=6)
        texto_1j = self.fuente_texto.render("1 JUGADOR", True, (255, 255, 255))
        pantalla.blit(texto_1j, (rect_1j.centerx - texto_1j.get_width() // 2,
                                  rect_1j.centery - texto_1j.get_height() // 2))

        
        return y + 55

    def _dibujar_nombre(self, pantalla, panel, y, foco):
        y = self._titulo_seccion(pantalla, panel, y, "2. NOMBRE DEL JUGADOR", foco)

        caja = pygame.Rect(panel.x + 20, y, panel.width - 40, 40)
        pygame.draw.rect(pantalla, (10, 12, 20), caja, border_radius=6)
        color_borde = self.AMARILLO_FOCO if foco else self.BORDE_PANEL
        pygame.draw.rect(pantalla, color_borde, caja, width=2, border_radius=6)

        texto_render = self.fuente_texto.render(self.texto, True, (255, 255, 255))
        pantalla.blit(texto_render, (caja.x + 12, caja.centery - texto_render.get_height() // 2))

        return y + 55

    def _dibujar_fila_personajes(self, pantalla, panel, y, titulo, miniaturas, indice, foco):
        y = self._titulo_seccion(pantalla, panel, y, titulo, foco)

        espacio = 16
        cantidad = len(miniaturas)
        tamano_img = miniaturas[0].get_width()
        ancho_slot = tamano_img + 16
        x_inicial = panel.centerx - (cantidad * ancho_slot + (cantidad - 1) * espacio) // 2

        for i, miniatura in enumerate(miniaturas):
            x = x_inicial + i * (ancho_slot + espacio)
            rect = pygame.Rect(x, y, ancho_slot, tamano_img + 16)

            elegido = (i == indice)
            if foco and elegido:
                color_borde, grosor = self.AMARILLO_FOCO, 4
            elif elegido:
                color_borde, grosor = self.VERDE_BORDE, 3
            else:
                color_borde, grosor = self.BORDE_PANEL, 2

            pygame.draw.rect(pantalla, self.PANEL_OSCURO, rect, border_radius=8)
            pantalla.blit(miniatura, (rect.centerx - tamano_img // 2, rect.centery - tamano_img // 2))
            pygame.draw.rect(pantalla, color_borde, rect, width=grosor, border_radius=8)

        return y + tamano_img + 16 + 15

    def _dibujar_botones(self, pantalla, panel, y):
        ancho_boton = (panel.width - 60) // 2

        rect_continuar = pygame.Rect(panel.x + 20, y, ancho_boton, 30)
        pygame.draw.rect(pantalla, self.VERDE_SELECCION, rect_continuar, border_radius=6)
        pygame.draw.rect(pantalla, self.VERDE_BORDE, rect_continuar, width=3, border_radius=6)
        texto_continuar = self.fuente_boton.render("CONTINUAR (ENTER)", True, (255, 255, 255))
        pantalla.blit(texto_continuar, (rect_continuar.centerx - texto_continuar.get_width() // 2,
                                         rect_continuar.centery - texto_continuar.get_height() // 2))

        rect_volver = pygame.Rect(rect_continuar.right + 20, y, ancho_boton, 30)
        pygame.draw.rect(pantalla, self.ROJO_BOTON, rect_volver, border_radius=6)
        pygame.draw.rect(pantalla, self.ROJO_BORDE, rect_volver, width=3, border_radius=6)
        texto_volver = self.fuente_boton.render("VOLVER (ESC)", True, (255, 255, 255))
        pantalla.blit(texto_volver, (rect_volver.centerx - texto_volver.get_width() // 2,
                                      rect_volver.centery - texto_volver.get_height() // 2))