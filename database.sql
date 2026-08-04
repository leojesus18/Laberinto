CREATE DATABASE IF NOT EXISTS laberinto_db;

USE laberinto_db;

CREATE TABLE IF NOT EXISTS puntajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_jugador VARCHAR(50) NOT NULL,
    tiempo_segundos FLOAT NOT NULL,
    dificultad VARCHAR(20) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);