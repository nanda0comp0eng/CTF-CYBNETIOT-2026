CREATE DATABASE IF NOT EXISTS movie_db;
USE movie_db;

CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255) NOT NULL,
    release_year INT,
    description TEXT,
    poster_url VARCHAR(255)
);

INSERT INTO movies (title, director, release_year, description, poster_url) VALUES
('The Matrix', 'Lana Wachowski, Lilly Wachowski', 1999, 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', 'http://localhost/fake'),
('Inception', 'Christopher Nolan', 2010, 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'http://localhost/fake'),
('Interstellar', 'Christopher Nolan', 2014, 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity''s survival.', 'http://localhost/fake'),
('Blade Runner 2049', 'Denis Villeneuve', 2017, 'A young Blade Runner''s discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who''s been missing for thirty years.', 'http://localhost/fake'),
('The Dark Knight', 'Christopher Nolan', 2008, 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 'http://localhost/fake');

-- CTF Flag Hidden in a separate table or as a comment
CREATE TABLE IF NOT EXISTS flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag_name VARCHAR(50),
    flag_value VARCHAR(255)
);

INSERT INTO flags (flag_name, flag_value) VALUES ('secret_flag', 'CYBNETIOT{siqil_InjekSion_Lowh_y4_CIK!}');
