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

game_over = False

while ejecutando:
    reloj.tick(FPS)

    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        if game_over:

            if evento.key == pygame.K_RETURN:
                jugador_x = jugador_inicio_x
                jugador_y = jugador_inicio_y

                cazador.reiniciar(
                    cazador_inicio_x,
                    cazador_inicio_y
                )

                game_over = False
            elif evento.key == pygame.K_ESCAPE:
                ejecutando = False

            continue    

    manejador_estados.manejar_eventos(eventos)
    manejador_estados.actualizar()
    manejador_estados.dibujar(pantalla)


    if game_over:

        fuente = pygame.font.SysFont(None, 50)

        texto = fuente.render(
            "GAME OVER",
            True,
            ROJO
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                ALTO // 2 - 50
            )
        )

        fuente2 = pygame.font.SysFont(None, 30)

        texto2 = fuente2.render(
            "ENTER para reiniciar",
            True,
            BLANCO
        )

        pantalla.blit(
            texto2,
            (
                ANCHO // 2 - texto2.get_width() // 2,
                ALTO // 2 + 10
            )
        )

    pygame.display.flip()

pygame.quit()
sys.exit()