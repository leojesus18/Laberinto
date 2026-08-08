from database.connection import ConexionDB


class ItemRepository:
    """
    Patrón Repository: encapsula todas las operaciones de las tablas
    'items' e 'inventario'. El resto del juego no escribe SQL directo,
    solo llama a estos métodos (guardar_item, usar_item, equipar_item...).
    """

    def __init__(self):
        self.conexion = ConexionDB()

    def guardar_item(self, nombre_jugador, tipo_item, cantidad=1):
        """Suma 'cantidad' unidades del ítem al inventario del jugador.
        Si es la primera vez que junta ese tipo de ítem, crea la fila;
        si ya tenía, actualiza sumando (ON DUPLICATE KEY UPDATE)."""
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            INSERT INTO inventario (nombre_jugador, item_id, cantidad)
            SELECT %s, id, %s FROM items WHERE tipo = %s
            ON DUPLICATE KEY UPDATE cantidad = cantidad + %s
            """,
            (nombre_jugador, cantidad, tipo_item, cantidad)
        )

        self.conexion.confirmar()

    def usar_item(self, nombre_jugador, tipo_item):
        """Consume 1 unidad del ítem. Si llega a 0, además se desequipa
        automáticamente (no tiene sentido tenerlo equipado sin stock)."""
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            UPDATE inventario inv
            JOIN items i ON i.id = inv.item_id
            SET inv.cantidad = inv.cantidad - 1,
                inv.equipado = IF(inv.cantidad - 1 <= 0, FALSE, inv.equipado)
            WHERE inv.nombre_jugador = %s AND i.tipo = %s AND inv.cantidad > 0
            """,
            (nombre_jugador, tipo_item)
        )

        self.conexion.confirmar()
        return cursor.rowcount > 0  # True si de verdad se consumió uno

    def equipar_item(self, nombre_jugador, tipo_item, equipado=True):
        """Marca (o desmarca) un ítem como equipado para ese jugador.
        Solo puede equiparse si tiene al menos 1 unidad en inventario."""
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            UPDATE inventario inv
            JOIN items i ON i.id = inv.item_id
            SET inv.equipado = %s
            WHERE inv.nombre_jugador = %s AND i.tipo = %s AND inv.cantidad > 0
            """,
            (equipado, nombre_jugador, tipo_item)
        )

        self.conexion.confirmar()
        return cursor.rowcount > 0

    def esta_equipado(self, nombre_jugador, tipo_item):
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            SELECT inv.equipado FROM inventario inv
            JOIN items i ON i.id = inv.item_id
            WHERE inv.nombre_jugador = %s AND i.tipo = %s
            """,
            (nombre_jugador, tipo_item)
        )

        fila = cursor.fetchone()
        return bool(fila[0]) if fila else False

    def obtener_inventario(self, nombre_jugador):
        """Devuelve la lista de ítems que tiene guardados ese jugador:
        [(nombre, tipo, cantidad, equipado), ...]"""
        cursor = self.conexion.obtener_cursor()

        cursor.execute(
            """
            SELECT i.nombre, i.tipo, inv.cantidad, inv.equipado
            FROM inventario inv
            JOIN items i ON i.id = inv.item_id
            WHERE inv.nombre_jugador = %s AND inv.cantidad > 0
            """,
            (nombre_jugador,)
        )

        return cursor.fetchall()