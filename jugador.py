import pygame
from constantes import *


class Jugador:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = AZUL

        # Estado que van completando los ítems del Factory Method
        # (ver patterns/factory/). Anto va a envolver estos efectos
        # con Decorator más adelante; por ahora quedan acá como estado
        # simple para que el sistema de ítems funcione de punta a punta.
        self.escudos = 0
        self.llaves = 0
        self._efectos_activos = {}  # nombre -> tiempo_fin_ms
        # Arranca en True para que, al activar lentitud, el PRIMER
        # movimiento se registre y el segundo se ignore (no al revés).
        self._ignorar_proximo_movimiento = True

    def mover(self, mapa, dx, dy):
        """Intenta mover al jugador dx, dy casillas. Respeta paredes,
        compuertas cerradas y bordes del mapa. Tiene en cuenta los
        efectos temporales activos (velocidad, lentitud, invertido)."""

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
        movió (útil para el buff de velocidad, que encadena 2 pasos)."""

        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        # Evita salir del mapa
        if not (0 <= nuevo_y < len(mapa) and 0 <= nuevo_x < len(mapa[0])):
            return False

        caracter = mapa[nuevo_y][nuevo_x]

        if caracter == "#":
            return False

        if caracter == "D":
            if self.llaves > 0:
                self.llaves -= 1
                # Se "abre" la compuerta: se reemplaza el carácter por
                # piso normal en esa fila del mapa.
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

    def recibir_golpe(self):
        """Llamado cuando el cazador atrapa al jugador. Si tiene un
        escudo, lo consume y evita perder una vida. Devuelve True si
        corresponde perder una vida, False si el escudo absorbió el golpe."""
        if self.escudos > 0:
            self.escudos -= 1
            return False

        return True

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
