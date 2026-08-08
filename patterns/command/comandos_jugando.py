from patterns.command.comando import Comando


class ComandoMover(Comando):

   #Mueve al jugador en una dirección (dx, dy). El receptor
   #(EstadoJugando) es quien realmente sabe mover/sonar/recolectar."""

    def __init__(self, estado_jugando, dx, dy):
        self.estado_jugando = estado_jugando
        self.dx = dx
        self.dy = dy

    def ejecutar(self):
        self.estado_jugando.mover_jugador(self.dx, self.dy)


class ComandoPausar(Comando):
   #Pausa el juego (tecla ESC)

    def __init__(self, estado_jugando):
        self.estado_jugando = estado_jugando

    def ejecutar(self):
        self.estado_jugando.pausar()


class ComandoEquiparEscudo(Comando):
   #Equipa/desequipa el escudo guardado en MySQL (tecla E)."""

    def __init__(self, estado_jugando):
        self.estado_jugando = estado_jugando

    def ejecutar(self):
        self.estado_jugando._alternar_equipo_escudo()