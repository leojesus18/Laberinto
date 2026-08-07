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