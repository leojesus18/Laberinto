# Escape del Laberinto

Trabajo Práctico Nº2 – Programación II (IES 9-023) — Videojuego desarrollado en Python con Pygame, aplicando patrones de diseño y persistencia de datos en MySQL.

---

## Integrantes

- Leonel Bustos
- Antonella Fernandez

---

## Descripción del juego

*Escape del Laberinto* es un juego de laberinto top-down (vista desde arriba) a través de **10 niveles** de dificultad creciente. El jugador debe recorrer cada laberinto recolectando llaves, escudos y power-ups, mientras es perseguido por un **cazador** controlado por una inteligencia artificial que persigue al jugador por el camino más corto y se vuelve más agresivo a medida que se avanza de nivel. El objetivo de cada nivel es alcanzar la salida sin quedarse sin vidas.

---

## Historia

Es de noche y las luces del instituto ya deberían estar apagadas. El jugador se quedó encerrado después de horario, y algo —o alguien— recorre los pasillos vacíos: el **Cazador**, una presencia que no da tregua. Piso por piso, aula por aula, hay que encontrar la salida antes de que te alcance. En el camino aparecen llaves para abrir puertas trabadas, escudos para resistir un encuentro, y objetos misteriosos que aceleran, frenan o confunden los propios pasos.

---

## Tecnologías usadas

| Tecnología | Uso en el proyecto |
|---|---|
| **Python 3** | Lenguaje principal |
| **Pygame** (`pygame>=2.6.0`) | Motor gráfico, game loop, manejo de eventos, sonido |
| **MySQL** | Persistencia de puntajes, inventario de ítems y su estado (usado/equipado) |
| **mysql-connector-python** (`>=9.0.0`) | Conexión de Python a MySQL |
| **python-dotenv** (`>=1.0.0`) | Carga de credenciales de base de datos desde un archivo `.env`, sin exponerlas en el repositorio |
| **Git / GitHub** | Control de versiones, ramas por integrante, Pull Requests |

---

## Instalación

1. **Cloná el repositorio:**
   ```bash
   git clone https://github.com/leojesus18/Laberinto.git
   cd Laberinto
   ```

2. **Creá un entorno virtual e instalá las dependencias:**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux / Mac

   pip install -r requirements.txt
   ```

3. **Creá la base de datos en MySQL** corriendo el script incluido:
   ```bash
   mysql -u root -p < database.sql
   ```
   Esto crea la base `laberinto_db` con las tablas `puntajes`, `items` e `inventario`.

4. **Configurá las credenciales de conexión.** Creá un archivo `.env` en la raíz del proyecto (no se sube a GitHub, está en `.gitignore`) con:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   DB_NAME=laberinto_db
   ```

---

## Ejecución

Con el entorno virtual activado y la base de datos ya creada:

```bash
python main.py
```

---

## Controles

| Tecla | Acción |
|---|---|
| ↑ ↓ ← → | Mover al jugador |
| **E** | Equipar / desequipar escudo |
| **ESC** | Pausar el juego |

*(Nota: si el jugador recolecta un ítem de "invertir controles", las flechas se invierten temporalmente como parte del efecto del ítem — no es un bug.)*

---


## Explicación de patrones

El juego aplica los 7 patrones de diseño pedidos por la consigna. Resumen de dónde y para qué se usa cada uno (detalle completo con fragmentos de código en `Informe_Patrones_Diseno_TP2.pdf`):

| Patrón | Dónde se usa | Carpeta |
|---|---|---|
| **Singleton** | Configuración global del juego, manejo de sonido, conexión a MySQL — una única instancia compartida de cada una en todo el programa | `patterns/singleton/`, `database/connection.py` |
| **Factory Method** | Creación de los 5 tipos de ítems (Escudo, Llave, Velocidad, Lentitud, Invertir) a partir del carácter que aparece en el mapa de cada nivel | `patterns/factory/` |
| **Observer** | `EstadisticasJugador` notifica cambios de vidas/escudos/llaves/puntaje; el `HUD` se suscribe y se actualiza solo, sin ir a consultar el estado en cada frame | `patterns/observer/` |
| **State** | Cada pantalla del juego (Portada, Menú, Dificultad, Nombre, Jugando, Pausa, Game Over, Victoria) es un estado independiente administrado por un `StateManager` | `patterns/state/` |
| **Strategy** | El nivel de agresividad del Cazador (qué tan rápido persigue) cambia según en qué nivel está el jugador, intercambiando el algoritmo sin tocar la clase `Cazador` | `patterns/strategy/` |
| **Command** | Cada tecla del jugador (mover, pausar, equipar escudo) es un objeto Comando con `ejecutar()`, en vez de una cadena de `if` sobre las teclas | `patterns/command/` |
| **Decorator** | Los power-ups temporales (velocidad, lentitud, invertir controles) envuelven dinámicamente el comportamiento de movimiento del jugador, pudiendo combinarse entre sí | `patterns/decorador/` |

---

## Explicación de base de datos

La persistencia usa **MySQL** con 3 tablas (definidas en `database.sql`) y el patrón **Repository** para separar el SQL del resto del juego:

- **`puntajes`** — guarda cada partida jugada: nombre del jugador, tiempo, puntaje final y dificultad. Se consulta para mostrar los mejores tiempos/puntajes (`ScoreRepository`).
- **`items`** — catálogo fijo de ítems persistibles (por ahora Escudo y Llave) con su nombre y descripción.
- **`inventario`** — cuánto de cada ítem tiene guardado cada jugador (por nombre) y si está *equipado* actualmente. Tiene una relación `FOREIGN KEY` hacia `items`.

`ItemRepository` (en `database/item_repository.py`) implementa las 3 operaciones que pide la consigna:

- **Guardar ítems** → `guardar_item()`: suma unidades al inventario del jugador (o crea el registro si es la primera vez).
- **Usar ítems** → `usar_item()`: descuenta una unidad; si llega a 0, se desequipa automáticamente.
- **Equipar ítems** → `equipar_item()` / `esta_equipado()`: marca un ítem como activo, solo si hay stock disponible.

`ScoreRepository` (en `database/score_repository.py`) maneja el guardado y la consulta de puntajes/tiempos de partidas jugadas.

Todas las consultas pasan por `ConexionDB` (patrón Singleton, ver sección de Patrones), que mantiene una única conexión activa a la base durante toda la ejecución del juego.