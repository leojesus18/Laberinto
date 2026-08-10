import pygame
from constantes import *
from collections import deque
from patterns.singleton.configuracion import Configuracion
from patterns.strategy.estrategia_cazador import obtener_estrategia_para_nivel
from sprites_personajes import cargar_sprites_direccionales, direccion_segun_movimiento

class Cazador:

    def __init__(self, x, y, indice_nivel=0):

        self.x = x
        self.y = y
        self.color = ROJO
        self.contador = 0

        clave_cazador = Configuracion().personaje_cazador
        self.sprites = cargar_sprites_direccionales(clave_cazador, int(TAM_CASILLA * 1.6))
        self.direccion = "frente"
        self.frame_animacion = 0  # índice del frame de caminata actual

        config = Configuracion()

        #El cazador se mueve mas rapido cuando las dificualtades son altas
        velocidades ={
            "facil":30,
            "normal":20,
            "dificil":10
        }

        frames_base = velocidades.get(config.dificultad, 20)

        # Strategy: por encima de la dificultad elegida en el menú, el
        # propio nivel exige más o menos agresividad (ver
        # patterns/strategy/estrategia_cazador.py).
        estrategia = obtener_estrategia_para_nivel(indice_nivel)
        self.frames_por_movimiento = estrategia.ajustar_frames(frames_base)

    def mover(self, mapa, jugador_x, jugador_y):

        self.contador += 1

        if self.contador < self.frames_por_movimiento:
            return

        self.contador = 0

        camino = self.encontrar_camino(
            mapa,
            jugador_x,
            jugador_y
        )

        # Si existe un camino...
        if len(camino) > 1:

            siguiente_x, siguiente_y = camino[1]

            dx = siguiente_x - self.x
            dy = siguiente_y - self.y
            self.direccion = direccion_segun_movimiento(dx, dy, self.direccion)

            self.x = siguiente_x
            self.y = siguiente_y

            cantidad_frames = len(self.sprites[self.direccion])
            self.frame_animacion = (self.frame_animacion + 1) % cantidad_frames

    def dibujar(self, pantalla):
        frames = self.sprites[self.direccion]
        sprite = frames[self.frame_animacion % len(frames)]
        x_centro = self.x * TAM_CASILLA + TAM_CASILLA // 2
        y_pie = self.y * TAM_CASILLA + TAM_CASILLA

        pantalla.blit(sprite, (
            x_centro - sprite.get_width() // 2,
            y_pie - sprite.get_height()
        ))


    def atrapo_jugador(self, jugador_x, jugador_y):

        return self.x == jugador_x and self.y == jugador_y
    
    def encontrar_camino(self, mapa, objetivo_x, objetivo_y):
        #Cola para almacenar las posiciones a explorar
        cola = deque()

        cola.append(
        (self.x, self.y)
        )
        #Diccionario para almacenar las posiciones visitadas y sus predecesores
        
        visitados = {}

        visitados[(self.x, self.y)] = None

        #El cazador puede moverse en 4 direcciones: derecha, izquierda, abajo y arriba
        movimientos = [
        (1,0),
        (-1,0),
        (0,1),           
        (0,-1)
        ]

        #Búsqueda en anchura (BFS) para encontrar el camino más corto
        while cola:

            actual_x, actual_y = cola.popleft() #Saca la primera posición de la cola


            if actual_x == objetivo_x and actual_y == objetivo_y:
                break  #Si se ha llegado al objetivo, se rompe el bucle


            for mov_x, mov_y in movimientos:  #Bucle para explorar las posiciones vecinas

                nuevo_x = actual_x + mov_x
                nuevo_y = actual_y + mov_y


                if (
                    nuevo_x >= 0 and
                    nuevo_y >= 0 and
                    nuevo_y < len(mapa) and   #Se asegura de que la nueva posición esté dentro de los límites del mapa
                    nuevo_x < len(mapa[0])
                ):

                    
                    if mapa[nuevo_y][nuevo_x] not in ("#", "D"):  #Asegura de que la nueva posición no sea una pared ni una compuerta cerrada

                        if (nuevo_x, nuevo_y) not in visitados:  #Asegura de que la nueva posición no haya sido visitada previamente

                            visitados[(nuevo_x, nuevo_y)] = (
                                actual_x,    #Almacena el predecesor de la nueva posición
                                actual_y     #Gracias a esto, se puede reconstruir el camino desde el objetivo hasta la posición inicial
                            )

                            
                            cola.append(
                                (nuevo_x, nuevo_y)
                            )

        if (objetivo_x, objetivo_y) not in visitados: #Si el objetivo no se ha alcanzado, significa que no hay camino posible, por lo que se devuelve una lista vacía
            return []

        camino = []

        actual = (
            objetivo_x,
            objetivo_y
        )


        while actual != None:  #Mientras la posición actual no sea None, se reconstruye el camino desde el objetivo hasta la posición inicial utilizando el diccionario de visitados

            camino.append(actual)

            actual = visitados.get(actual)


        camino.reverse()       #Se invierte el camino para que vaya desde la posición inicial hasta el objetivo


        return camino
    
    
    