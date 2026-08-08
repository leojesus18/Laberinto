from abc import ABC, abstractmethod


class Comando(ABC):
    
   #Patrón Command: cada tecla del juego se convierte en un objeto
   #con un método ejecutar(), en vez de un montón de "if tecla == X"
   #sueltos adentro de manejar_eventos. El objeto Comando no sabe
   #CÓMO se mueve el jugador o cómo se pausa el juego, solo le pide
   #al "receptor" (EstadoJugando) que lo haga.

    @abstractmethod
    def ejecutar(self):
        raise NotImplementedError