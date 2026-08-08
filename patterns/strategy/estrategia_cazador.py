from abc import ABC, abstractmethod


class EstrategiaCazador(ABC):
    """
    Patrón Strategy.

    Cazador ya calcula sus frames_por_movimiento en base a la
    dificultad elegida en el menú (facil/normal/dificil, ver
    Configuracion). Esta jerarquía agrega un segundo eje: qué tan
    agresivo es el cazador según el NIVEL en el que está el jugador,
    sin tener que meter un montón de "if nivel == X" adentro de
    Cazador. Cazador solo le pregunta a su estrategia actual
    "¿cuántos frames me hacés esperar?" y no le importa cuál sea.
    """

    @abstractmethod
    def ajustar_frames(self, frames_base):
        """Recibe los frames_por_movimiento que salieron de la
        dificultad del menú y devuelve el valor final a usar."""
        raise NotImplementedError


class EstrategiaEstandar(EstrategiaCazador):
    """Niveles de introducción (1 a 3): el cazador se comporta tal
    cual la dificultad elegida en el menú, sin bonus extra."""

    def ajustar_frames(self, frames_base):
        return frames_base


class EstrategiaAgresiva(EstrategiaCazador):
    """Niveles intermedios (4 a 6): el cazador persigue más rápido
    de lo que pediría la dificultad del menú sola."""

    FRAMES_MINIMOS = 6

    def ajustar_frames(self, frames_base):
        return max(self.FRAMES_MINIMOS, frames_base - 8)


class EstrategiaImplacable(EstrategiaCazador):
    """Niveles avanzados (7 a 10): el cazador persigue casi al doble
    de velocidad de lo normal - para estos niveles, esquivarlo importa
    más que la velocidad del jugador."""

    FRAMES_MINIMOS = 3

    def ajustar_frames(self, frames_base):
        return max(self.FRAMES_MINIMOS, frames_base // 2)


def obtener_estrategia_para_nivel(indice_nivel):
    """indice_nivel es 0-based (0 = nivel1, 9 = nivel10)."""
    numero_nivel = indice_nivel + 1

    if numero_nivel <= 3:
        return EstrategiaEstandar()
    elif numero_nivel <= 6:
        return EstrategiaAgresiva()
    else:
        return EstrategiaImplacable()
