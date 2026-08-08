import random
from collections import deque

# ---------------------------------------------------------------------------
# Generador de laberintos "perfectos" (spanning tree: un único camino entre
# dos celdas cualquiera, sin loops) via recursive backtracker. Después se
# le agregan ítems y compuertas respetando reglas que garantizan que el
# nivel siempre se pueda terminar.
# ---------------------------------------------------------------------------


def generar_grilla(ancho_celdas, alto_celdas, rng):
    ancho = ancho_celdas * 2 + 1
    alto = alto_celdas * 2 + 1
    grilla = [["#"] * ancho for _ in range(alto)]

    def celda_a_pixel(cx, cy):
        return (cx * 2 + 1, cy * 2 + 1)

    visitado = [[False] * ancho_celdas for _ in range(alto_celdas)]
    pila = [(0, 0)]
    visitado[0][0] = True

    while pila:
        cx, cy = pila[-1]
        px, py = celda_a_pixel(cx, cy)
        grilla[py][px] = "."

        vecinos = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < ancho_celdas and 0 <= ny < alto_celdas and not visitado[ny][nx]:
                vecinos.append((nx, ny, dx, dy))

        if not vecinos:
            pila.pop()
            continue

        nx, ny, dx, dy = rng.choice(vecinos)
        # Tira abajo la pared entre la celda actual y la vecina elegida
        grilla[py + dy][px + dx] = "."
        npx, npy = celda_a_pixel(nx, ny)
        grilla[npy][npx] = "."
        visitado[ny][nx] = True
        pila.append((nx, ny))

    return grilla


def calcular_regiones(grilla, bloqueadas):
    """Etiqueta cada celda de piso con un número de "región", tratando
    las celdas en `bloqueadas` (las futuras puertas) como paredes. En
    un laberinto perfecto (árbol), esto separa el mapa en tantas
    regiones como puertas + 1 (P-side, entre puerta 1 y 2, ..., S-side).
    Se usa para agregar loops SOLO dentro de cada región, nunca entre
    regiones distintas - así el jugador gana caminos alternativos para
    esquivar al cazador, pero seguís necesitando la llave para cruzar
    de una región a la siguiente."""
    alto, ancho = len(grilla), len(grilla[0])
    region_de = {}
    contador_region = 0

    for y in range(alto):
        for x in range(ancho):
            if grilla[y][x] != "#" and (x, y) not in bloqueadas and (x, y) not in region_de:
                cola = deque([(x, y)])
                region_de[(x, y)] = contador_region
                while cola:
                    cx, cy = cola.popleft()
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = cx + dx, cy + dy
                        if (0 <= nx < ancho and 0 <= ny < alto
                                and grilla[ny][nx] != "#"
                                and (nx, ny) not in bloqueadas
                                and (nx, ny) not in region_de):
                            region_de[(nx, ny)] = contador_region
                            cola.append((nx, ny))
                contador_region += 1

    return region_de


def agregar_bifurcaciones(grilla, region_de, rng, porcentaje):
    """Tira abajo un porcentaje de paredes "internas" (las que separan
    dos celdas de la MISMA región) para que el laberinto deje de ser un
    árbol puro y tenga caminos alternativos - sin esto, el jugador
    nunca puede esquivar al cazador en un pasillo (un árbol tiene un
    único camino posible entre dos puntos cualquiera)."""
    alto, ancho = len(grilla), len(grilla[0])
    candidatos = []

    # Paredes que separan dos celdas en horizontal (x par, y impar)
    for y in range(1, alto - 1, 2):
        for x in range(2, ancho - 2, 2):
            if grilla[y][x] == "#":
                a, b = (x - 1, y), (x + 1, y)
                if grilla[y][a[0]] != "#" and grilla[y][b[0]] != "#":
                    ra, rb = region_de.get(a), region_de.get(b)
                    if ra is not None and ra == rb:
                        candidatos.append((x, y))

    # Paredes que separan dos celdas en vertical (x impar, y par)
    for x in range(1, ancho - 1, 2):
        for y in range(2, alto - 2, 2):
            if grilla[y][x] == "#":
                a, b = (x, y - 1), (x, y + 1)
                if grilla[a[1]][x] != "#" and grilla[b[1]][x] != "#":
                    ra, rb = region_de.get(a), region_de.get(b)
                    if ra is not None and ra == rb:
                        candidatos.append((x, y))

    rng.shuffle(candidatos)
    cantidad = int(len(candidatos) * porcentaje)
    for (x, y) in candidatos[:cantidad]:
        grilla[y][x] = "."


def bfs_camino(grilla, inicio, bloqueados=frozenset(), objetivo=None):
    """BFS genérico. Si se pasa `objetivo`, corta apenas lo encuentra y
    devuelve el camino. Si no, devuelve el diccionario de distancias
    completo (para buscar la celda más lejana)."""
    alto, ancho = len(grilla), len(grilla[0])
    visitados = {inicio: None}
    cola = deque([inicio])

    while cola:
        actual = cola.popleft()
        if objetivo is not None and actual == objetivo:
            break
        ax, ay = actual
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = ax + dx, ay + dy
            if 0 <= nx < ancho and 0 <= ny < alto and grilla[ny][nx] != "#" and (nx, ny) not in bloqueados:
                if (nx, ny) not in visitados:
                    visitados[(nx, ny)] = actual
                    cola.append((nx, ny))

    if objetivo is not None:
        if objetivo not in visitados:
            return None
        camino = []
        actual = objetivo
        while actual is not None:
            camino.append(actual)
            actual = visitados[actual]
        camino.reverse()
        return camino

    return visitados


def generar_nivel(ancho_celdas, alto_celdas, num_puertas, cant_E, cant_V, cant_L, cant_I, semilla, porcentaje_loops=0.20):
    rng = random.Random(semilla)

    for intento in range(200):
        grilla = generar_grilla(ancho_celdas, alto_celdas, rng)
        inicio = (1, 1)
        alto, ancho = len(grilla), len(grilla[0])

        distancias = bfs_camino(grilla, inicio)
        # La salida es la celda más lejana del inicio (recorrido más largo posible)
        salida = max(distancias.keys(), key=lambda c: _longitud_camino(distancias, c))
        camino_completo = bfs_camino(grilla, inicio, objetivo=salida)

        if len(camino_completo) < num_puertas * 3 + 6:
            continue  # camino muy corto para meter tantas puertas, se regenera

        # Elegimo posiciones de puertas repartidas a lo largo del camino,
        # evitando los extremos (nunca pegadas a P ni a S).
        indices_disponibles = list(range(3, len(camino_completo) - 3))
        if len(indices_disponibles) < num_puertas:
            continue
        rng.shuffle(indices_disponibles)
        indices_puertas = sorted(indices_disponibles[:num_puertas])

        # Evita puertas pegadas entre sí (para que cada tramo tenga margen)
        if any(indices_puertas[i + 1] - indices_puertas[i] < 3 for i in range(len(indices_puertas) - 1)):
            continue

        puertas = [camino_completo[i] for i in indices_puertas]

        # Zona "antes de cualquier puerta": BFS desde el inicio tratando
        # TODAS las puertas como pared. Ahí, y solo ahí, van las llaves.
        zona_previa = bfs_camino(grilla, inicio, bloqueados=frozenset(puertas))
        celdas_para_llaves = [
            c for c in zona_previa
            if c != inicio and grilla[c[1]][c[0]] != "#" and c not in puertas
        ]

        if len(celdas_para_llaves) < num_puertas:
            continue  # no entran todas las llaves antes de la primera puerta

        rng.shuffle(celdas_para_llaves)
        llaves = celdas_para_llaves[:num_puertas]

        # Agregar bifurcaciones (loops) DENTRO de cada región (separadas
        # por las puertas), para que el jugador tenga caminos alternativos
        # y pueda esquivar al cazador. Nunca conecta dos regiones distintas,
        # así que la mecánica de "necesitás la llave para cruzar" sigue
        # intacta - solo cambia que cada tramo deja de ser un pasillo único.
        region_de = calcular_regiones(grilla, bloqueadas=frozenset(puertas))
        agregar_bifurcaciones(grilla, region_de, rng, porcentaje=porcentaje_loops)

        # El resto de los ítems (buenos y malos) van en cualquier piso libre
        # del mapa completo (recalculado DESPUÉS del braiding, que agregó
        # celdas de piso nuevas), ya que una vez que tenés todas las llaves
        # necesarias podés recorrer cualquier parte del laberinto.
        ocupadas = {inicio, salida, *puertas, *llaves}
        celdas_libres = [
            (x, y)
            for y in range(alto) for x in range(ancho)
            if grilla[y][x] != "#" and (x, y) not in ocupadas
        ]

        total_items_extra = cant_E + cant_V + cant_L + cant_I
        if len(celdas_libres) < total_items_extra:
            continue

        rng.shuffle(celdas_libres)
        idx = 0
        posiciones_E = celdas_libres[idx: idx + cant_E]; idx += cant_E
        posiciones_V = celdas_libres[idx: idx + cant_V]; idx += cant_V
        posiciones_L = celdas_libres[idx: idx + cant_L]; idx += cant_L
        posiciones_I = celdas_libres[idx: idx + cant_I]; idx += cant_I

        # ---- Volcar todo a la grilla de caracteres ----
        for (x, y) in puertas:
            grilla[y][x] = "D"
        for (x, y) in llaves:
            grilla[y][x] = "K"
        for (x, y) in posiciones_E:
            grilla[y][x] = "E"
        for (x, y) in posiciones_V:
            grilla[y][x] = "V"
        for (x, y) in posiciones_L:
            grilla[y][x] = "L"
        for (x, y) in posiciones_I:
            grilla[y][x] = "I"

        grilla[inicio[1]][inicio[0]] = "P"
        grilla[salida[1]][salida[0]] = "S"

        # Posición inicial del cazador: una celda lejana del jugador
        # (para que no arranque encima), pero que no sea ninguna de las
        # celdas ya usadas por la salida, puertas, llaves o ítems.
        usadas = {inicio, salida, *puertas, *llaves,
                  *posiciones_E, *posiciones_V, *posiciones_L, *posiciones_I}
        candidatos_cazador = sorted(
            (c for c in distancias if c not in usadas),
            key=lambda c: -_longitud_camino(distancias, c)
        )
        if not candidatos_cazador:
            continue
        cazador_pos = candidatos_cazador[len(candidatos_cazador) // 3]  # lejos, pero no exactamente en la salida
        grilla[cazador_pos[1]][cazador_pos[0]] = "C"

        filas = ["".join(fila) for fila in grilla]

        if _validar_nivel(filas, num_puertas):
            return filas

    raise RuntimeError("No se pudo generar un nivel válido con estos parámetros")


def _longitud_camino(distancias, celda):
    largo = 0
    actual = celda
    while distancias[actual] is not None:
        largo += 1
        actual = distancias[actual]
    return largo


def _validar_nivel(filas, num_puertas_esperadas):
    """Valida, leyendo el nivel ya armado (como lo haría el juego real),
    que: 1) todas las llaves se puedan juntar sin cruzar ninguna puerta,
    y 2) con esa cantidad de llaves, se puede llegar de P a S."""
    grilla = [list(f) for f in filas]
    alto, ancho = len(grilla), len(grilla[0])

    inicio = salida = None
    puertas, llaves = [], []

    for y in range(alto):
        for x in range(ancho):
            c = grilla[y][x]
            if c == "P":
                inicio = (x, y)
            elif c == "S":
                salida = (x, y)
            elif c == "D":
                puertas.append((x, y))
            elif c == "K":
                llaves.append((x, y))

    if inicio is None or salida is None:
        return False
    if len(puertas) != num_puertas_esperadas or len(llaves) != num_puertas_esperadas:
        return False

    zona_previa = bfs_camino(filas_a_grilla_bloqueos(filas), inicio, bloqueados=frozenset(puertas))
    if not all(k in zona_previa for k in llaves):
        return False  # alguna llave quedó detrás de una puerta: inválido

    conectividad_total = bfs_camino(filas_a_grilla_bloqueos(filas), inicio)  # puertas como piso normal
    if salida not in conectividad_total:
        return False  # ni siquiera hay camino físico (no debería pasar nunca)

    return True


def filas_a_grilla_bloqueos(filas):
    # bfs_camino ya trata cualquier carácter que no sea "#" como piso
    # transitable (P, S, K, D, E, V, L, I incluidos); la restricción real
    # de las puertas se aplica aparte, pasando `bloqueados` en bfs_camino.
    return [list(f) for f in filas]


CONFIG_NIVELES = {
    # nivel: (ancho_celdas, alto_celdas, puertas, E, V, L, I, % de loops)
    2:  (8,  4, 1, 1, 1, 1, 0, 0.28),
    3:  (8,  5, 1, 1, 1, 1, 1, 0.26),
    4:  (9,  5, 2, 2, 1, 1, 1, 0.24),
    5:  (9,  6, 2, 2, 2, 2, 1, 0.22),
    6:  (10, 6, 2, 2, 2, 2, 2, 0.20),
    7:  (10, 7, 3, 2, 2, 3, 2, 0.18),
    8:  (11, 7, 3, 3, 2, 3, 3, 0.16),
    9:  (11, 7, 3, 3, 3, 4, 3, 0.14),
    10: (11, 7, 4, 3, 3, 5, 4, 0.12),
}

resultado = {}
for nivel, (aw, ah, puertas, e, v, l, i, pct_loops) in CONFIG_NIVELES.items():
    filas = generar_nivel(aw, ah, puertas, e, v, l, i, semilla=1000 + nivel, porcentaje_loops=pct_loops)
    resultado[nivel] = filas
    print(f"nivel{nivel}: {len(filas[0])}x{len(filas)}  puertas={puertas}  E={e} V={v} L={l} I={i}  loops={pct_loops:.0%}  -> OK")

# Volcado en formato Python listo para pegar en niveles.py
with open("niveles_generados.py", "w") as f:
    for nivel, filas in resultado.items():
        f.write(f"nivel{nivel} = [\n")
        for fila in filas:
            f.write(f'"{fila}",\n')
        f.write("]\n\n")

print("\nArchivo niveles_generados.py escrito OK")
