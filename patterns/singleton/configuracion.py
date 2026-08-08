class Configuracion:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        # Estos valores solo se setean la primera vez que se crea la instancia
        self.volumen_musica = 0.5
        self.volumen_sonido = 0.7
        self.dificultad ="facil"     # puede ser "facil", "normal", "dificil"
        self.nombre_jugador = ""     # se completa en EstadoNombre antes de jugar