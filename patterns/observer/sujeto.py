class Sujeto:
    """
    Patrón Observer - lado "Sujeto" (Subject/Observable).

    Mantiene la lista de observadores suscriptos y los notifica cuando
    algo cambia. No sabe nada de pygame ni de cómo se dibuja el HUD:
    solo avisa "esto cambió a tal valor" y quien esté escuchando decide
    qué hacer con esa información.
    """

    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def quitar_observador(self, observador):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self, evento, datos=None):
        for observador in self._observadores:
            observador.actualizar(evento, datos)
