import pygame
from constantes import *
from patterns.decorador.comportamiento_movimiento import (
    ComportamientoMovimiento,
    DecoradorVelocidad,
    DecoradorLentitud,
    DecoradorInvertido,
)


class Jugador:

    def __init__(self, x, y, estadisticas):
        self.x = x
        self.y = y
        self.color = AZUL

        # EstadisticasJugador (patrón Observer, ver patterns/observer/)
        # es la única fuente de verdad para vidas/escudos/llaves. El HUD
        # observa esta misma instancia, así que cualquier cambio hecho
        # acá (recibir_golpe, abrir una compuerta) se refleja solo en
        # pantalla sin que Jugador sepa que existe un HUD.
        self.estadisticas = estadisticas

        self._efectos_activos = {}  # nombre -> tiempo_fin_ms
        # Arranca en True para que, al activar lentitud, el PRIMER
        # movimiento se registre y el segundo se ignore (no al revés).
        self._ignorar_proximo_movimiento = True

    def mover(self, mapa, dx, dy):
       #Intenta mover al jugador dx, dy casillas. Respeta paredes,
       #compuertas cerradas y bordes del mapa. Los efectos temporales
       #(velocidad/lentitud/invertido) se aplican envolviendo el
       #movimiento base con decoradores (patrón Decorator) según qué
       #efectos estén activos en este momento."""

        comportamiento = ComportamientoMovimiento()

        if self._tiene_efecto("velocidad"):
            comportamiento = DecoradorVelocidad(comportamiento)
        if self._tiene_efecto("lentitud"):
            comportamiento = DecoradorLentitud(comportamiento)
        if self._tiene_efecto("invertido"):
            comportamiento = DecoradorInvertido(comportamiento)

        comportamiento.mover(self, mapa, dx, dy)

    def _mover_una_casilla(self, mapa, dx, dy):
       #Mueve una sola casilla si es posible. Devuelve True si se
       #movió (útil para el buff de velocidad, que encadena 2 pasos)."""

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
       #Llamado por Item.aplicar_efecto() cuando el jugador
       #recolecta un ítem de velocidad/lentitud/invertir."""
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
       #Devuelve {nombre_efecto: segundos_restantes} de los efectos
       #temporales activos (velocidad/lentitud/invertido), para que el
       #HUD le avise al jugador qué le está pasando y por qué."""
        ahora = pygame.time.get_ticks()
        restantes = {}

        for nombre, tiempo_fin in list(self._efectos_activos.items()):
            if ahora < tiempo_fin:
                restantes[nombre] = (tiempo_fin - ahora) / 1000
            else:
                del self._efectos_activos[nombre]

        return restantes

    def recibir_golpe(self, escudo_equipado=True):
       #Llamado cuando el cazador atrapa al jugador. Si tiene un
       #escudo Y lo tiene equipado, lo consume y evita perder una vida."""
        if self.estadisticas.escudos > 0 and escudo_equipado:
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
