import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class ConexionDB:
    """
    Patrón Singleton aplicado a la conexión con la base de datos.
    Los datos de conexión se leen del archivo .env (que no se sube a GitHub),
    así cada integrante del grupo usa su propia contraseña sin exponerla.
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._conectar()
        return cls._instancia

    def _conectar(self):
        self.conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    def obtener_cursor(self):
        return self.conexion.cursor()

    def confirmar(self):
        self.conexion.commit()