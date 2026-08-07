import pygame
from patterns.observer.observador import Observador
from constantes import *


class HUD(Observador):
    
    #Observador concreto: se suscribe a un EstadisticasJugador y guarda su PROPIA copia de vidas/escudos/llaves/puntaje.

    
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
