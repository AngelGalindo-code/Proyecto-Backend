CREATE DATABASE ProDe;
USE ProDe;

CREATE TABLE partidos (
	id_partido INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    fase VARCHAR(50)
    );

CREATE TABLE usuarios (
	id_usuario INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usuario VARCHAR(50),
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    puntos INT
	);
    
CREATE TABLE resultados (
	id_partido INT NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    FOREIGN KEY (id_partido) REFERENCES partidos(id_partido)
	);

CREATE TABLE predicciones (
	id_usuario INT NOT NULL,
    id_partido INT NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY(id_partido) REFERENCES partidos(id_partido)
    );


