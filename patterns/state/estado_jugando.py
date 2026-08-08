import pygame
from patterns.state.estado import Estado
from jugador import Jugador
from cazador import Cazador
from constantes import *
from niveles import nivel1
from patterns.factory.item_factory import generar_items_desde_mapa
from patterns.observer.estadisticas_jugador import EstadisticasJugador
from patterns.observer.hud import HUD
from database.item_repository import ItemRepository
from patterns.singleton.configuracion import Configuracion


class EstadoJugando(Estado):

    def __init__(self, manejador_estados):
        super().__init__(manejador_estados)
        # list(nivel1) copia la lista de filas: así, si el jugador abre
        # una compuerta, se modifica esta copia y no el mapa original de
        # niveles.py (que se reutilizaría "roto" en la próxima partida).
        self.mapa = list(nivel1)

        jugador_x, jugador_y, cazador_x, cazador_y = self._buscar_posiciones_iniciales()

        # EstadisticasJugador es el Sujeto (patrón Observer): guarda
        # vidas/escudos/llaves/puntaje y notifica a quien esté
        # suscripto (el HUD) cada vez que algo cambia.
        self.estadisticas = EstadisticasJugador(vidas_iniciales=3)
        self.hud = HUD(self.estadisticas)  # el HUD se suscribe solo, en su __init__

        self.jugador = Jugador(jugador_x, jugador_y, self.estadisticas)
        self.cazador = Cazador(cazador_x, cazador_y)
        self.items = generar_items_desde_mapa(self.mapa)
        self.tiempo_inicio = pygame.time.get_ticks()

        from patterns.singleton.sound_manager import SoundManager
        self.sonido = SoundManager()
        self.sonido.reproducir_musica(self.sonido.musica_juego)

    def _buscar_posiciones_iniciales(self):
        jugador_x = jugador_y = 0
        cazador_x = cazador_y = 0

        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):
                if self.mapa[fila][columna] == "P":
                    jugador_x, jugador_y = columna, fila
                elif self.mapa[fila][columna] == "C":
                    cazador_x, cazador_y = columna, fila

        return jugador_x, jugador_y, cazador_x, cazador_y

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    from patterns.state.estado_pausa import EstadoPausa
                    self.manejador_estados.cambiar_estado(
                        EstadoPausa(self.manejador_estados, self)
                    )
                    return

                if evento.key == pygame.K_e:
                    self._alternar_equipo_escudo()
                    return

                dx = dy = 0
                if evento.key == pygame.K_UP:
                    dy = -1
                elif evento.key == pygame.K_DOWN:
                    dy = 1
                elif evento.key == pygame.K_LEFT:
                    dx = -1
                elif evento.key == pygame.K_RIGHT:
                    dx = 1

                if dx != 0 or dy != 0:
                    self.jugador.mover(self.mapa, dx, dy)
                    self.sonido.reproducir_sonido(self.sonido.sonido_movimiento_jugador)
                    self._recolectar_item_si_corresponde()

                    if self.jugador.llego_a_salida(self.mapa):
                        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) / 1000

                        from patterns.state.estado_victoria import EstadoVictoria
                        self.manejador_estados.cambiar_estado(
                            EstadoVictoria(
                                self.manejador_estados,
                                tiempo_transcurrido,
                                self.estadisticas.puntaje
                            )
                        )

    def _recolectar_item_si_corresponde(self):
        for item in self.items:
            if item.recolectado:
                continue

            if item.x == self.jugador.x and item.y == self.jugador.y:
                item.aplicar_efecto(self.jugador)
                item.recolectado = True

                if item.puntos:
                    self.estadisticas.sumar_puntos(item.puntos)

                # Persistencia en MySQL: solo escudo y llave se guardan
                # en el inventario (Repository), los demás son efectos
                # temporales de una sola partida y no se guardan.
                if getattr(item, "tipo", None) in ("escudo", "llave"):
                    nombre = Configuracion().nombre_jugador
                    ItemRepository().guardar_item(nombre, item.tipo, 1)

                self.sonido.reproducir_sonido(self.sonido.sonido_movimiento_jugador)

    def _alternar_equipo_escudo(self):
        """Tecla E: equipa o desequipa el escudo (patrón Repository,
        persiste en MySQL). Solo se puede equipar si hay stock."""
        if self.estadisticas.escudos <= 0:
            return

        nombre = Configuracion().nombre_jugador
        repositorio = ItemRepository()
        equipado_actual = repositorio.esta_equipado(nombre, "escudo")
        repositorio.equipar_item(nombre, "escudo", not equipado_actual)
        self.sonido.reproducir_sonido(self.sonido.sonido_movimiento_jugador)


    def actualizar(self):
        self.cazador.mover(self.mapa, self.jugador.x, self.jugador.y)

        if self.cazador.atrapo_jugador(self.jugador.x, self.jugador.y):
            self.sonido.reproducir_sonido(self.sonido.sonido_movimiento_cazador)

            nombre = Configuracion().nombre_jugador
            escudo_equipado = ItemRepository().esta_equipado(nombre, "escudo")

            self.jugador.recibir_golpe(escudo_equipado)  # actualiza estadisticas y notifica al HUD solo

            if escudo_equipado and self.estadisticas.escudos >= 0:
                ItemRepository().usar_item(nombre, "escudo")

            if self.estadisticas.vidas <= 0:
                from patterns.state.estado_gameover import EstadoGameOver
                self.manejador_estados.cambiar_estado(
                    EstadoGameOver(self.manejador_estados)
                )
            else:
                jugador_x, jugador_y, cazador_x, cazador_y = self._buscar_posiciones_iniciales()
                self.jugador.x = jugador_x
                self.jugador.y = jugador_y
                self.cazador.x = cazador_x
                self.cazador.y = cazador_y

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):
                caracter = self.mapa[fila][columna]

                rect = pygame.Rect(
                    columna * TAM_CASILLA,
                    fila * TAM_CASILLA,
                    TAM_CASILLA,
                    TAM_CASILLA
                )

                if caracter == "#":
                    pygame.draw.rect(pantalla, GRIS, rect)
                elif caracter == "S":
                    pygame.draw.rect(pantalla, VERDE, rect)
                elif caracter == "D":
                    pygame.draw.rect(pantalla, MARRON_OSCURO, rect)
                else:
                    pygame.draw.rect(pantalla, BLANCO, rect)

        for item in self.items:
            item.dibujar(pantalla)

        self.jugador.dibujar(pantalla)
        self.cazador.dibujar(pantalla)

        self.hud.dibujar(pantalla)  # HUD: se dibuja con lo que le llegó por notificación, no lee nada acá

        # Avisar en pantalla qué efecto temporal está activo y por cuánto,
        # para que un debuff (lentitud/invertido) no se sienta como que
        # el juego se trabó. Esto es transitorio y no forma parte de las
        # estadísticas "persistentes" del Observer.

        if self.estadisticas.escudos > 0:
            equipado = ItemRepository().esta_equipado(Configuracion().nombre_jugador, "escudo")
            texto_escudo = "Escudo: EQUIPADO (E)" if equipado else "Escudo: guardado (E para equipar)"
            color_escudo = VERDE if equipado else GRIS
            fuente_escudo = pygame.font.SysFont(None, 22)
            render_escudo = fuente_escudo.render(texto_escudo, True, color_escudo)
            pantalla.blit(render_escudo, (10, ALTO - 30))
                
        NOMBRES_EFECTO = {
            "velocidad": ("Velocidad+", VERDE_CLARO),
            "lentitud": ("Lentitud", MARRON),
            "invertido": ("Controles invertidos", VIOLETA),
        }
        fuente_efectos = pygame.font.SysFont(None, 24)
        fila_y = 40
        for nombre, segundos in self.jugador.efectos_activos_restantes().items():
            etiqueta, color = NOMBRES_EFECTO.get(nombre, (nombre, BLANCO))
            texto_efecto = fuente_efectos.render(f"{etiqueta} ({segundos:.1f}s)", True, color)
            pantalla.blit(texto_efecto, (10, fila_y))
            fila_y += 22
