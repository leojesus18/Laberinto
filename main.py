import pygame
import sys
from cazador import Cazador

from constantes import *
from niveles import nivel1

pygame.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Escape del Laberinto")

reloj = pygame.time.Clock()

# ==========================
# BUSCAR POSICIONES INICIALES
# ==========================

jugador_x = 0
jugador_y = 0

cazador_x = 0
cazador_y = 0

for fila in range(len(nivel1)):
    for columna in range(len(nivel1[fila])):

        if nivel1[fila][columna] == "P":
            jugador_x = columna
            jugador_y = fila

        elif nivel1[fila][columna] == "C":
            cazador_x = columna
            cazador_y = fila

# ==========================
# CREAR OBJETO CAZADOR
# ==========================
cazador = Cazador(cazador_x, cazador_y)

contador = 0

ejecutando = True

while ejecutando:

    reloj.tick(FPS)

    contador += 1

    # ==========================
    # EVENTOS
    # ==========================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            nuevo_x = jugador_x
            nuevo_y = jugador_y

            if evento.key == pygame.K_UP:
                nuevo_y -= 1

            elif evento.key == pygame.K_DOWN:
                nuevo_y += 1

            elif evento.key == pygame.K_LEFT:
                nuevo_x -= 1

            elif evento.key == pygame.K_RIGHT:
                nuevo_x += 1

            # Evita salir del mapa
            if (
                0 <= nuevo_y < len(nivel1)
                and
                0 <= nuevo_x < len(nivel1[0])
            ):

                # Evita atravesar paredes
                if nivel1[nuevo_y][nuevo_x] != "#":

                    jugador_x = nuevo_x
                    jugador_y = nuevo_y

                    # Llegó a la salida
                    if nivel1[jugador_y][jugador_x] == "S":
                        print("¡Nivel completado!")

    cazador.mover(
    nivel1,
    jugador_x,
    jugador_y
    )

    # ==========================
    # GAME OVER
    # ==========================

    if cazador.atrapo_jugador(jugador_x, jugador_y):

        print("GAME OVER")

        ejecutando = False

    # ==========================
    # DIBUJAR
    # ==========================

    pantalla.fill(NEGRO)

    for fila in range(len(nivel1)):
        for columna in range(len(nivel1[fila])):

            caracter = nivel1[fila][columna]

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

            else:
                pygame.draw.rect(pantalla, BLANCO, rect)

    # Jugador
    pygame.draw.circle(
        pantalla,
        AZUL,
        (
            jugador_x * TAM_CASILLA + TAM_CASILLA // 2,
            jugador_y * TAM_CASILLA + TAM_CASILLA // 2
        ),
        TAM_CASILLA // 3
    )

    # Cazador
    cazador.dibujar(pantalla)

    pygame.display.flip()

pygame.quit()
sys.exit()