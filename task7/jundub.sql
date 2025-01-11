CREATE TABLE credit_cards_numbers (
    id SERIAL PRIMARY KEY,
    card_number TEXT
);
INSERT INTO credit_cards_numbers (card_number)
VALUES ('1234-5678-9876-5432');
DROP DATABASE jundb;
CREATE DATABASE jundb;