import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def _obtener_variable(*nombres_posibles):
    """Busca la primera variable de entorno que exista entre varios
    nombres posibles. Esto evita que el proyecto se rompa porque cada
    integrante nombró su .env de manera diferente.
    """
    for nombre in nombres_posibles:
        valor = os.getenv(nombre)
        if valor is not None and valor != "":
            return valor
    return None


class ConexionDB:
    """
    Patrón Singleton aplicado a la conexión con la base de datos.
    Los datos de conexión se leen del archivo .env (que no se sube a GitHub),
    así cada integrante del grupo usa su propia contraseña sin exponerla.
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            nueva_instancia = super().__new__(cls)
            nueva_instancia._conectar()  # si esto lanza una excepción, NO se guarda como
            cls._instancia = nueva_instancia  # instancia rota: la próxima llamada reintenta
        return cls._instancia

    def _conectar(self):
        host = _obtener_variable("DB_HOST", "MYSQL_HOST")
        puerto = _obtener_variable("DB_PORT", "MYSQL_PORT")
        usuario = _obtener_variable("DB_USER", "MYSQL_USER", "DB_USUARIO")
        contrasena = _obtener_variable("DB_PASSWORD", "MYSQL_PASSWORD", "DB_CONTRASENA")
        base = _obtener_variable("DB_NAME", "DB_DATABASE", "MYSQL_DATABASE")

        faltantes = [
            nombre for nombre, valor in [
                ("host", host), ("puerto", puerto), ("usuario", usuario),
                ("contraseña", contrasena), ("base de datos", base),
            ] if valor is None
        ]
        if faltantes:
            raise RuntimeError(
                "Faltan variables en el .env para conectar a MySQL: "
                + ", ".join(faltantes)
                + ". Revisá que existan DB_HOST, DB_PORT, DB_USER, DB_PASSWORD y DB_NAME."
            )

        self.conexion = mysql.connector.connect(
            host=host,
            port=int(puerto),
            user=usuario,
            password=contrasena,
            database=base
        )

    def obtener_cursor(self):
        return self.conexion.cursor()

    def confirmar(self):
        self.conexion.commit()