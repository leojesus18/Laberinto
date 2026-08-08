from patterns.observer.sujeto import Sujeto


class EstadisticasJugador(Sujeto):
    """
    Sujeto concreto del patrón Observer.

    Es la única fuente de verdad para vidas, escudos, llaves y puntaje.
    Jugador (para la lógica de compuertas/escudo) y HUD (para mostrarlos
    en pantalla) apuntan los dos a la MISMA instancia de esta clase -
    así nunca se desincronizan entre sí.

    Cada método que cambia un valor termina en notificar(...), que es lo
    que dispara Observador.actualizar(...) en todo lo que esté
    suscripto (por ahora, el HUD).
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

    def reiniciar_llaves(self):
        """Se llama al pasar de nivel: las llaves son específicas de las
        compuertas de CADA laberinto, así que no tiene sentido arrastrarlas
        de un mapa a otro (vidas, escudos y puntaje sí se mantienen)."""
        self.llaves = 0
        self.notificar("llaves", self.llaves)

    def sumar_puntos(self, cantidad):
        self.puntaje += cantidad
        self.notificar("puntaje", self.puntaje)
