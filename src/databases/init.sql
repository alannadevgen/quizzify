-- This file is used to create the tables in the database when the server starts up.
-- The tables are only created if they do not already exist in the database.

-- Table artists
-- id, name, popularity
-- DROP TABLE IF EXISTS artists;
CREATE TABLE artists (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    popularity INT
);

-- Table users
-- id, username, email, hashed_pwd, created_at, image_url, spotify_uri
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    hashed_pwd BYTEA,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table spotify_users: fetch user information from Spotify API
DROP TABLE IF EXISTS spotify_users;
CREATE TABLE spotify_users (
    spotify_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    spotify_username VARCHAR(100),
    spotify_email VARCHAR(150),
    spotify_image_url VARCHAR(100),
    spotify_uri VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
