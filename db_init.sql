CREATE DATABASE bankdb;
USE bankdb;

CREATE TABLE accounts(
    account_no INT PRIMARY KEY,
    name VARCHAR(50),
    balance FLOAT
);

CREATE TABLE transactions(
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no INT,
    type VARCHAR(20),
    amount FLOAT,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
show tables;
DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    pin VARCHAR(4),
    balance DECIMAL(10,2)
);
CREATE DATABASE IF NOT EXISTS bankdb;
USE bankdb;

CREATE TABLE IF NOT EXISTS accounts (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    pin VARCHAR(4),
    balance DECIMAL(10,2)
);
INSERT INTO accounts (id, name, username, pin, balance)
VALUES (3, 'shinchan ji', 'shinu', '2211', 10);
USE bankdb;  -- make sure you are using your bank database

SELECT COUNT(*) AS total_accounts FROM accounts;

