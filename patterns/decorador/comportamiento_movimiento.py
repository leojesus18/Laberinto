class ComportamientoMovimiento:
    
   #Patrón Decorator: este es el "componente base" - el movimiento
   #normal, sin ningún efecto. Los power-ups temporales (velocidad,
   #lentitud, invertido) se implementan como decoradores que ENVUELVEN
   #a este comportamiento (o a otro decorador), agregando su propio
   #efecto antes o después de llamar al que envuelven.


    def mover(self, jugador, mapa, dx, dy):
        jugador._mover_una_casilla(mapa, dx, dy)


class DecoradorMovimiento(ComportamientoMovimiento):
   #Base común de todos los decoradores: guardan una referencia al
   #comportamiento que están envolviendo (self.envuelto)."""

    def __init__(self, envuelto):
        self.envuelto = envuelto


class DecoradorVelocidad(DecoradorMovimiento):
   #Ítem de velocidad: se mueve el doble (2 casillas por tecla)."""

    def mover(self, jugador, mapa, dx, dy):
        self.envuelto.mover(jugador, mapa, dx, dy)
        self.envuelto.mover(jugador, mapa, dx, dy)


class DecoradorLentitud(DecoradorMovimiento):
   #Ítem de lentitud (debuff): ignora un movimiento de cada dos."""

    def mover(self, jugador, mapa, dx, dy):
        jugador._ignorar_proximo_movimiento = not jugador._ignorar_proximo_movimiento
        if jugador._ignorar_proximo_movimiento:
            return
        self.envuelto.mover(jugador, mapa, dx, dy)


class DecoradorInvertido(DecoradorMovimiento):
   #Ítem de invertir controles (debuff): invierte la dirección."""

    def mover(self, jugador, mapa, dx, dy):
        self.envuelto.mover(jugador, mapa, -dx, -dy)