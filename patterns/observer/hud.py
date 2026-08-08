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

    def __init__(self, estadisticas):
        self.vidas = estadisticas.vidas
        self.escudos = estadisticas.escudos
        self.llaves = estadisticas.llaves
        self.puntaje = estadisticas.puntaje

        estadisticas.agregar_observador(self)

        self._fuente = pygame.font.SysFont(None, 28)

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
        texto = self._fuente.render(
            f"Vidas: {self.vidas}   Escudos: {self.escudos}   "
            f"Llaves: {self.llaves}   Puntos: {self.puntaje}",
            True, BLANCO
        )
        pantalla.blit(texto, (10, 10))
