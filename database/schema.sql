CREATE DATABASE IF NOT EXISTS cricket_ticketing;
USE cricket_ticketing;

CREATE TABLE matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_a VARCHAR(100) NOT NULL,
    team_b VARCHAR(100) NOT NULL,
    match_date DATETIME NOT NULL,
    total_tickets INT NOT NULL,
    available_tickets INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
