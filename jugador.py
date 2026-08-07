import pygame
from constantes import *


class Jugador:

    def __init__(self, x, y, estadisticas):
        self.x = x
        self.y = y
        self.color = AZUL

        
        self.estadisticas = estadisticas

        self._efectos_activos = {}  
        
        self._ignorar_proximo_movimiento = True

    def mover(self, mapa, dx, dy):
        
        if self._tiene_efecto("invertido"):
            dx, dy = -dx, -dy

        if self._tiene_efecto("lentitud"):
            # Se ignora un movimiento de cada dos
            self._ignorar_proximo_movimiento = not self._ignorar_proximo_movimiento
            if self._ignorar_proximo_movimiento:
                return

        pasos = 2 if self._tiene_efecto("velocidad") else 1

        for _ in range(pasos):
            if not self._mover_una_casilla(mapa, dx, dy):
                break

    def _mover_una_casilla(self, mapa, dx, dy):
        """Mueve una sola casilla si es posible. Devuelve True si se
        movió """

        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        # Evita salir del mapa
        if not (0 <= nuevo_y < len(mapa) and 0 <= nuevo_x < len(mapa[0])):
            return False

        caracter = mapa[nuevo_y][nuevo_x]

        if caracter == "#":
            return False

        if caracter == "D":
            if self.estadisticas.llaves > 0:
                self.estadisticas.usar_llave()
                mapa[nuevo_y] = (
                    mapa[nuevo_y][:nuevo_x] + "." + mapa[nuevo_y][nuevo_x + 1:]
                )
            else:
                return False  # compuerta cerrada, falta llave

        self.x = nuevo_x
        self.y = nuevo_y
        return True

    def activar_efecto_temporal(self, nombre, duracion_ms):
        """Llamado por Item.aplicar_efecto() cuando el jugador
        recolecta un ítem de velocidad/lentitud/invertir."""
        self._efectos_activos[nombre] = pygame.time.get_ticks() + duracion_ms

    def _tiene_efecto(self, nombre):
        tiempo_fin = self._efectos_activos.get(nombre)

        if tiempo_fin is None:
            return False

        if pygame.time.get_ticks() >= tiempo_fin:
            del self._efectos_activos[nombre]
            return False

        return True

    def efectos_activos_restantes(self):
        """Devuelve {nombre_efecto: segundos_restantes} de los efectos
        temporales activos (velocidad/lentitud/invertido), para que el
        HUD le avise al jugador qué le está pasando y por qué."""
        ahora = pygame.time.get_ticks()
        restantes = {}

        for nombre, tiempo_fin in list(self._efectos_activos.items()):
            if ahora < tiempo_fin:
                restantes[nombre] = (tiempo_fin - ahora) / 1000
            else:
                del self._efectos_activos[nombre]

        return restantes

    def recibir_golpe(self):
        """Llamado cuando el cazador atrapa al jugador. Si tiene un
        escudo, lo consume y evita perder una vida."""
        if self.estadisticas.escudos > 0:
            self.estadisticas.usar_escudo()
        else:
            self.estadisticas.perder_vida()

    def llego_a_salida(self, mapa):
        return mapa[self.y][self.x] == "S"

    def dibujar(self, pantalla):
        pygame.draw.circle(
            pantalla,
            self.color,
            (
                self.x * TAM_CASILLA + TAM_CASILLA // 2,
                self.y * TAM_CASILLA + TAM_CASILLA // 2
            ),
            TAM_CASILLA // 3
        )
