from abc import ABC, abstractmethod

from patterns.factory.item import (
    ItemEscudo,
    ItemLlave,
    ItemVelocidad,
    ItemLentitud,
    ItemInvertir,
)


class ItemFactory(ABC):
    """
    Patrón Factory Method.

    Esta clase abstracta define el "molde" para crear ítems: obliga a
    cada fábrica concreta a implementar crear_item(x, y). El código que
    genera los ítems de un nivel (ver generar_items_desde_mapa, más abajo)
    solo llama a fabrica.crear_item(x, y) sin importar ni conocer las
    clases concretas de Item - así se puede agregar un ítem nuevo sin
    tocar ni una línea de estado_jugando.py.
    """

    @abstractmethod
    def crear_item(self, x, y):
        raise NotImplementedError


class FabricaEscudo(ItemFactory):
    def crear_item(self, x, y):
        return ItemEscudo(x, y)


class FabricaLlave(ItemFactory):
    def crear_item(self, x, y):
        return ItemLlave(x, y)


class FabricaVelocidad(ItemFactory):
    def crear_item(self, x, y):
        return ItemVelocidad(x, y)


class FabricaLentitud(ItemFactory):
    def crear_item(self, x, y):
        return ItemLentitud(x, y)


class FabricaInvertir(ItemFactory):
    def crear_item(self, x, y):
        return ItemInvertir(x, y)


# Mapeo carácter del mapa -> fábrica que sabe crear ese ítem.
# Para sumar un ítem nuevo el día de mañana: crear la clase Item en
# item.py, la fábrica acá arriba, y agregar una línea en este diccionario.
FABRICAS_POR_CARACTER = {
    "E": FabricaEscudo(),
    "K": FabricaLlave(),
    "V": FabricaVelocidad(),
    "L": FabricaLentitud(),
    "I": FabricaInvertir(),
}

# Caracteres de ítems que existen para que niveles.py y estado_jugando.py
# los usen sin tener que repetir la lista a mano.
CARACTERES_ITEMS = tuple(FABRICAS_POR_CARACTER.keys())


def generar_items_desde_mapa(mapa):
    """Recorre el mapa y usa la fábrica correspondiente a cada carácter
    de ítem para instanciar la lista de ítems de ese nivel."""
    items = []

    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            caracter = mapa[fila][columna]
            fabrica = FABRICAS_POR_CARACTER.get(caracter)

            if fabrica is not None:
                items.append(fabrica.crear_item(columna, fila))

    return items
