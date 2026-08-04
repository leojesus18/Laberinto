import pygame
import sys

from constantes import ANCHO, ALTO, FPS
from core.state_manager import StateManager
from patterns.state.estado_menu import EstadoMenu

pygame.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Escape del Laberinto")

reloj = pygame.time.Clock()

manejador_estados = StateManager()
manejador_estados.cambiar_estado(EstadoMenu(manejador_estados))

ejecutando = True

while ejecutando:
    reloj.tick(FPS)

    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            ejecutando = False

    manejador_estados.manejar_eventos(eventos)
    manejador_estados.actualizar()
    manejador_estados.dibujar(pantalla)

    pygame.display.flip()

pygame.quit()
sys.exit()