from database.connection import ConexionDB


class ScoreRepository:

   #Patrón Repository: encapsula todas las operaciones de la tabla 'puntajes'.

    def __init__(self):
        self.conexion = ConexionDB()

    def guardar_puntaje(self, nombre_jugador, tiempo_segundos, puntaje, dificultad):
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            INSERT INTO puntajes (nombre_jugador, tiempo_segundos, puntaje, dificultad)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre_jugador, tiempo_segundos, puntaje, dificultad)
        )

        self.conexion.confirmar()

    def obtener_mejores_tiempos(self, cantidad=5):
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            SELECT nombre_jugador, tiempo_segundos, puntaje, dificultad, fecha
            FROM puntajes
            ORDER BY tiempo_segundos ASC
            LIMIT %s
            """,
            (cantidad,)
        )

        return cursor.fetchall()

    def obtener_mejores_puntajes(self, cantidad=5):
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            SELECT nombre_jugador, tiempo_segundos, puntaje, dificultad, fecha
            FROM puntajes
            ORDER BY puntaje DESC
            LIMIT %s
            """,
            (cantidad,)
        )

        return cursor.fetchall()
