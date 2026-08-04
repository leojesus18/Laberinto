class Estado:
    
    
    #Cada estado del juego: Menu, Jugando, Pausa, GameOver, Victoria.
    #hereda de esta clase y define su propio comportamiento para estos 3 métodos. 
    #El juego no necesita saber en qué estado está: simplemente
    #llama a estos 3 métodos en cada vuelta del game loop.
    

    def __init__(self, manejador_estados):
        self.manejador_estados = manejador_estados

    def manejar_eventos(self, eventos):
        #Recibe la lista de eventos de pygame como teclas, quit, etc.
        pass

    def actualizar(self):
        # La lógica que se ejecuta cada frame
        pass

    def dibujar(self, pantalla):
        #Dibuja lo que corresponda a este estado en pantalla
        pass