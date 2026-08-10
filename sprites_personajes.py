import os
import pygame

DIRECCIONES = ["frente", "espalda", "perfil_izquierda", "perfil_derecha"]


def cargar_sprites_direccionales(clave_personaje, alto_objetivo):
   #Carga los frames de caminata de un personaje para sus 4 direcciones y
   #los escala manteniendo la proporción para que todas midan 'alto_objetivo'
   #de alto. Devuelve un diccionario {direccion: [frame_0, frame_1, ...]}
   #Si existen frames de animación en disco (ej: cazador_frente_0.png,
   #cazador_frente_1.png, ...) se cargan todos, en orden. Si el personaje
   #todavía no tiene frames de caminata (falta procesarlos), se usa como
   #único frame la imagen estática de siempre (cazador_frente.png), para
   #que ese personaje se vea quieto pero el juego no se rompa.

    sprites = {}

    for direccion in DIRECCIONES:
        rutas_frames = []
        indice = 0
        while True:
            ruta = f"assets/images/personajes/{clave_personaje}_{direccion}_{indice}.png"
            if not os.path.exists(ruta):
                break
            rutas_frames.append(ruta)
            indice += 1

        if not rutas_frames:
            rutas_frames = [f"assets/images/personajes/{clave_personaje}_{direccion}.png"]

        superficies = []
        for ruta in rutas_frames:
            imagen = pygame.image.load(ruta).convert_alpha()

            escala = alto_objetivo / imagen.get_height()
            ancho_nuevo = int(imagen.get_width() * escala)

            superficies.append(
                pygame.transform.smoothscale(imagen, (ancho_nuevo, alto_objetivo))
            )

        sprites[direccion] = superficies

    return sprites


def direccion_segun_movimiento(dx, dy, direccion_actual):
   #Traduce un movimiento (dx, dy) a una de las 4 direcciones delsprite. Si no hubo movimiento (dx=dy=0), mantiene la direcciónen la que ya estaba mirando el personaje
    if dy > 0:
        return "frente"
    if dy < 0:
        return "espalda"
    if dx < 0:
        return "perfil_izquierda"
    if dx > 0:
        return "perfil_derecha"
    return direccion_actual