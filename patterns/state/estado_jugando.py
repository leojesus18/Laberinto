import pygame
from patterns.state.estado import Estado
from jugador import Jugador
from cazador import Cazador
from constantes import *
from niveles import NIVELES
from patterns.factory.item_factory import generar_items_desde_mapa
from patterns.observer.estadisticas_jugador import EstadisticasJugador
from patterns.observer.hud import HUD
from database.item_repository import ItemRepository
from patterns.singleton.configuracion import Configuracion
from patterns.command.comandos_jugando import ComandoMover, ComandoPausar, ComandoEquiparEscudo


class EstadoJugando(Estado):

    def __init__(self, manejador_estados, indice_nivel=0, estadisticas=None, hud=None):
        super().__init__(manejador_estados)

        # indice_nivel es 0-based (0 = nivel1 ... 9 = nivel10).
        self.indice_nivel = indice_nivel

        # list(...) copia la lista de filas: así, si el jugador abre una
        # compuerta, se modifica esta copia y no el mapa original de
        # niveles.py (que se reutilizaría "roto" en la próxima partida).
        self.mapa = list(NIVELES[indice_nivel])

        jugador_x, jugador_y, cazador_x, cazador_y = self._buscar_posiciones_iniciales()

        # EstadisticasJugador es el Sujeto (patrón Observer): guarda
        # vidas/escudos/llaves/puntaje y notifica a quien esté
        # suscripto (el HUD) cada vez que algo cambia.
        # Si viene de un nivel anterior (estadisticas/hud no son None),
        # seguimos usando la MISMA instancia: vidas, escudos y puntaje
        # se arrastran de nivel a nivel (una partida real, no 10 partidas
        # sueltas). Las llaves sí se reinician: son específicas de las
        # compuertas de cada laberinto.
        if estadisticas is None:
            self.estadisticas = EstadisticasJugador(vidas_iniciales=3)
        else:
            self.estadisticas = estadisticas
            self.estadisticas.reiniciar_llaves()

        self.hud = hud if hud is not None else HUD(self.estadisticas)

        self.jugador = Jugador(jugador_x, jugador_y, self.estadisticas)
        self.cazador = Cazador(cazador_x, cazador_y, indice_nivel)
        self.items = generar_items_desde_mapa(self.mapa)
        self.tiempo_inicio = pygame.time.get_ticks()

        from patterns.singleton.sound_manager import SoundManager
        self.sonido = SoundManager()
        self.sonido.reproducir_musica(self.sonido.musica_juego)

        # Se crean UNA sola vez acá, no en dibujar() (que corre ~60
        # veces por segundo): crear una fuente por frame es innecesario
        # y de las cosas que más suman a que un juego 2D "ande lento".
        self._fuente_efectos = pygame.font.SysFont(None, 24)
        self._NOMBRES_EFECTO = {
            "velocidad": ("Velocidad+", VERDE_CLARO),
            "lentitud": ("Lentitud", MARRON),
            "invertido": ("Controles invertidos", VIOLETA),
        }

        # Patrón Command: cada tecla queda asociada a un objeto Comando.
        # manejar_eventos ya no tiene que saber CÓMO se mueve el jugador
        # o cómo se pausa, solo busca el comando de la tecla y lo ejecuta.
        self.comandos = {
            pygame.K_UP: ComandoMover(self, 0, -1),
            pygame.K_DOWN: ComandoMover(self, 0, 1),
            pygame.K_LEFT: ComandoMover(self, -1, 0),
            pygame.K_RIGHT: ComandoMover(self, 1, 0),
            pygame.K_ESCAPE: ComandoPausar(self),
            pygame.K_e: ComandoEquiparEscudo(self),
        }

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
                comando = self.comandos.get(evento.key)
                if comando:
                    comando.ejecutar()

    def mover_jugador(self, dx, dy):
       #Receptor del ComandoMover: mueve al jugador, reproduce el
       #sonido de paso, revisa si recolectó algo, y si llegó a la
       #salida pasa a la pantalla de victoria.
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
                    self.estadisticas,
                    self.hud,
                    self.indice_nivel
                )
            )

    def pausar(self):
       #Receptor del ComandoPausar
        from patterns.state.estado_pausa import EstadoPausa
        self.manejador_estados.cambiar_estado(
            EstadoPausa(self.manejador_estados, self)
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

        # Mostrar información del escudo
        if self.estadisticas.escudos > 0:
            equipado = ItemRepository().esta_equipado(
                Configuracion().nombre_jugador,
                "escudo"
            )

            texto_escudo = (
                "Escudo: EQUIPADO (E)"
                if equipado
                else "Escudo: guardado (E para equipar)"
            )

            color_escudo = VERDE if equipado else GRIS

            fuente_escudo = pygame.font.SysFont(None, 22)

            render_escudo = fuente_escudo.render(
                texto_escudo,
                True,
                color_escudo
            )

            pantalla.blit(
                render_escudo,
                (10, ALTO - 30)
            )

        # Mostrar efectos temporales activos
        fila_y = 40

        for nombre, segundos in self.jugador.efectos_activos_restantes().items():
            etiqueta, color = self._NOMBRES_EFECTO.get(
                nombre,
                (nombre, BLANCO)
            )

            texto_efecto = self._fuente_efectos.render(
                f"{etiqueta} ({segundos:.1f}s)",
                True,
                color
            )

            pantalla.blit(
                texto_efecto,
                (10, fila_y)
            )

            fila_y += 22