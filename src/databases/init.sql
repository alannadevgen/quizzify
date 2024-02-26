-- This file is used to create the tables in the database when the server starts up.
-- The tables are only created if they do not already exist in the database.

-- Table artists
-- id, name, popularity
--DROP TABLE IF EXISTS artists;
--CREATE TABLE IF NOT EXISTS artists (
CREATE TABLE artists (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    popularity INT
);

-- Table users
-- id, username, email, hashed_pwd
--DROP TABLE IF EXISTS users;
--CREATE TABLE IF NOT EXISTS users (
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(150),
    hashed_pwd VARCHAR(100)
);