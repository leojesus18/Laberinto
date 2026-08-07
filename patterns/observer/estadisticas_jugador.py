from patterns.observer.sujeto import Sujeto


class EstadisticasJugador(Sujeto):
    """
    Sujeto concreto del patrón Observer.

    Es la única fuente de verdad para vidas, escudos, llaves y puntaje.
    
    """

    def __init__(self, vidas_iniciales=3):
        super().__init__()
        self.vidas = vidas_iniciales
        self.escudos = 0
        self.llaves = 0
        self.puntaje = 0

    def perder_vida(self):
        self.vidas -= 1
        self.notificar("vidas", self.vidas)

    def ganar_escudo(self):
        self.escudos += 1
        self.notificar("escudos", self.escudos)

    def usar_escudo(self):
        self.escudos -= 1
        self.notificar("escudos", self.escudos)

    def ganar_llave(self):
        self.llaves += 1
        self.notificar("llaves", self.llaves)

    def usar_llave(self):
        self.llaves -= 1
        self.notificar("llaves", self.llaves)

    def sumar_puntos(self, cantidad):
        self.puntaje += cantidad
        self.notificar("puntaje", self.puntaje)
