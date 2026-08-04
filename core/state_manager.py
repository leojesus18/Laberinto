class StateManager:
    
    #Administra en qué estado (pantalla) está el juego actualmente.
    #permite cambiar de pantallas
    # Llama a los 3 métodos (manejar_eventos, actualizar, dibujar), decide que hacer con cada uno

    def __init__(self):
        self.estado_actual = None

    def cambiar_estado(self, nuevo_estado):
        self.estado_actual = nuevo_estado

    def manejar_eventos(self, eventos):
        if self.estado_actual:
            self.estado_actual.manejar_eventos(eventos)

    def actualizar(self):
        if self.estado_actual:
            self.estado_actual.actualizar()

    def dibujar(self, pantalla):
        if self.estado_actual:
            self.estado_actual.dibujar(pantalla)