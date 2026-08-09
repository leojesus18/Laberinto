import pygame

DIRECCIONES = ["frente", "espalda", "perfil_izquierda", "perfil_derecha"]


def cargar_sprites_direccionales(clave_personaje, alto_objetivo):
   #Carga las 4 imágenes direccionales de un personaje y las escala manteniendo la proporción para que todas midan 'alto_objetivo' de alto.
   #Devuelve un diccionario {direccion: superficie_pygame}

    sprites = {}

    for direccion in DIRECCIONES:
        ruta = f"assets/images/personajes/{clave_personaje}_{direccion}.png"
        imagen = pygame.image.load(ruta).convert_alpha()

        escala = alto_objetivo / imagen.get_height()
        ancho_nuevo = int(imagen.get_width() * escala)

        sprites[direccion] = pygame.transform.smoothscale(
            imagen, (ancho_nuevo, alto_objetivo)
        )

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