CREATE DATABASE IF NOT EXISTS laberinto_db;

USE laberinto_db;

CREATE TABLE IF NOT EXISTS puntajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_jugador VARCHAR(50) NOT NULL,
    tiempo_segundos FLOAT NOT NULL,
    puntaje INT NOT NULL DEFAULT 0,
    dificultad VARCHAR(20) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Si la tabla 'puntajes' ya existía de antes (de una base creada antes
-- de sumar el sistema de puntaje), correr esto una sola vez a mano:
-- ALTER TABLE puntajes ADD COLUMN puntaje INT NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(20) NOT NULL UNIQUE,
    descripcion VARCHAR(150)
);

INSERT INTO items (nombre, tipo, descripcion) VALUES
    ('Escudo', 'escudo', 'Aguanta un encuentro con el cazador sin perder vida'),
    ('Llave', 'llave', 'Abre una compuerta del laberinto');

CREATE TABLE IF NOT EXISTS inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_jugador VARCHAR(50) NOT NULL,
    item_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 0,
    equipado BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE KEY jugador_item (nombre_jugador, item_id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);