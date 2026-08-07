from abc import ABC, abstractmethod


class Observador(ABC):
    

    @abstractmethod
    def actualizar(self, evento, datos):
        #Llamado por el Sujeto cada vez que notifica un cambio.`evento` es un string "
        raise NotImplementedError
