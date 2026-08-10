import pygame
from patterns.observer.observador import Observador
from constantes import *


class HUD(Observador):
    """
    Observador concreto: se suscribe a un EstadisticasJugador (Sujeto)
    y guarda su PROPIA copia de vidas/escudos/llaves/puntaje.

    La diferencia clave con la versión anterior (que leía
    self.jugador.escudos directo en cada dibujar()) es que acá el HUD
    nunca va a buscar el dato: EstadisticasJugador se lo empuja apenas
    cambia, vía actualizar(). Si mañana el puntaje se actualiza 50
    veces en un frame, el HUD igual solo termina mostrando el último
    valor, sin acoplarse a cómo ni cuándo cambió.
    """

    PANEL_OSCURO = (20, 26, 40)
    BORDE_PANEL = (90, 100, 130)
    ROJO_VIDA = (220, 60, 70)
    CELESTE_ESCUDO = (100, 200, 255)
    AMARILLO_LLAVE = (255, 215, 0)
    NARANJA_PUNTOS = (255, 180, 60)

    def __init__(self, estadisticas):
        self.vidas = estadisticas.vidas
        self.escudos = estadisticas.escudos
        self.llaves = estadisticas.llaves
        self.puntaje = estadisticas.puntaje

        estadisticas.agregar_observador(self)

        self._fuente = pygame.font.SysFont("arial", 24, bold=True)

    def actualizar(self, evento, datos):
        if evento == "vidas":
            self.vidas = datos
        elif evento == "escudos":
            self.escudos = datos
        elif evento == "llaves":
            self.llaves = datos
        elif evento == "puntaje":
            self.puntaje = datos

    def dibujar(self, pantalla):
        ancho_panel = self._calcular_ancho_necesario()
        panel = pygame.Rect(10, 10, ancho_panel, 44)
        pygame.draw.rect(pantalla, self.PANEL_OSCURO, panel, border_radius=10)
        pygame.draw.rect(pantalla, self.BORDE_PANEL, panel, width=2, border_radius=10)

        x = panel.x + 16
        y_centro = panel.centery

        x = self._dibujar_grupo(pantalla, x, y_centro, self._dibujar_corazon,
                                 self.ROJO_VIDA, self.vidas)
        x = self._dibujar_grupo(pantalla, x, y_centro, self._dibujar_escudo,
                                 self.CELESTE_ESCUDO, self.escudos)
        x = self._dibujar_grupo(pantalla, x, y_centro, self._dibujar_llave,
                                 self.AMARILLO_LLAVE, self.llaves)
        x = self._dibujar_grupo(pantalla, x, y_centro, self._dibujar_estrella,
                                 self.NARANJA_PUNTOS, self.puntaje)

    def _calcular_ancho_necesario(self):
        """El panel se agranda solo si el puntaje (u otro valor)
        llega a varios dígitos, para que el número nunca quede
        pegado al borde ni se salga del panel."""
        ancho = 16  # padding izquierdo
        for valor in (self.vidas, self.escudos, self.llaves, self.puntaje):
            ancho += 26  # ícono
            ancho += self._fuente.size(str(valor))[0]
            ancho += 22  # separación entre grupos
        return max(ancho + 10, 200)

    def _dibujar_grupo(self, pantalla, x, y_centro, funcion_icono, color, valor):
        """Dibuja un ícono + su número al lado, y devuelve la
        posición x donde debería arrancar el próximo grupo."""
        funcion_icono(pantalla, x, y_centro, color)
        x += 26

        texto = self._fuente.render(str(valor), True, (255, 255, 255))
        pantalla.blit(texto, (x, y_centro - texto.get_height() // 2))
        x += texto.get_width() + 22

        return x

    def _dibujar_corazon(self, pantalla, x, y_centro, color):
        radio = 6
        pygame.draw.circle(pantalla, color, (x + radio, y_centro - 3), radio)
        pygame.draw.circle(pantalla, color, (x + radio * 3, y_centro - 3), radio)
        pygame.draw.polygon(pantalla, color, [
            (x - 1, y_centro - 2),
            (x + radio * 4 + 1, y_centro - 2),
            (x + radio * 2, y_centro + 11),
        ])

    def _dibujar_escudo(self, pantalla, x, y_centro, color):
        ancho, alto = 18, 20
        y0 = y_centro - alto // 2
        pygame.draw.polygon(pantalla, color, [
            (x, y0),
            (x + ancho, y0),
            (x + ancho, y0 + alto * 0.55),
            (x + ancho // 2, y0 + alto),
            (x, y0 + alto * 0.55),
        ])

    def _dibujar_llave(self, pantalla, x, y_centro, color):
        pygame.draw.circle(pantalla, color, (x + 6, y_centro), 6, width=3)
        pygame.draw.rect(pantalla, color, (x + 10, y_centro - 2, 12, 4))
        pygame.draw.rect(pantalla, color, (x + 18, y_centro + 2, 3, 5))

    def _dibujar_estrella(self, pantalla, x, y_centro, color):
        import math
        cx, cy, radio_ext, radio_int = x + 10, y_centro, 11, 5
        puntos = []
        for i in range(10):
            angulo = math.pi / 2 + i * math.pi / 5
            radio = radio_ext if i % 2 == 0 else radio_int
            puntos.append((cx + radio * math.cos(angulo), cy - radio * math.sin(angulo)))
        pygame.draw.polygon(pantalla, color, puntos)