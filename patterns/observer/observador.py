from abc import ABC, abstractmethod


class Observador(ABC):
    """
    Patrón Observer - lado "Observador".

    Cualquier cosa que necesite enterarse en tiempo real de cambios en
    las estadísticas del jugador (vidas, escudos, llaves, puntaje)
    implementa esta interfaz y se suscribe a un Sujeto (ver sujeto.py).
    El HUD (ver hud.py) es el observador concreto que usamos ahora,
    pero mañana podría sumarse otro (por ejemplo, un logro que se
    dispara al llegar a cierto puntaje) sin tocar EstadisticasJugador.
    """

    @abstractmethod
    def actualizar(self, evento, datos):
        """Llamado por el Sujeto cada vez que notifica un cambio.
        `evento` es un string ("vidas", "escudos", "llaves", "puntaje")
        y `datos` es el nuevo valor."""
        raise NotImplementedError
