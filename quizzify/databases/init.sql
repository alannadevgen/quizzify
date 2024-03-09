-- This file is used to create the tables in the database when the server starts up.
-- The tables are only created if they do not already exist in the database.

-- Relation Albums

-- column_name  |     data_type
----------------+-------------------
-- id           | character varying
-- name         | character varying
-- artist_id    | character varying, foreign key
-- popularity   | integer
-- release_date | date
-- total_tracks | integer

DROP TABLE IF EXISTS albums;

CREATE TABLE albums (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    artist_id VARCHAR(100),
    popularity INT,
    release_date DATE,
    total_tracks INT,
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------

-- Relation Artists

-- column_name |     data_type
---------------+-------------------
-- id          | character varying
-- name        | character varying
-- popularity  | integer
-- image_url   | character varying

-- DROP TABLE IF EXISTS artists;
CREATE TABLE artists (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    popularity INT,
    image_url VARCHAR(150)
);

----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------

-- Relation Songs
-- column_name  |     data_type
----------------+-------------------
-- id           | character varying
-- name         | character varying
-- artist_id    | character varying, foreign key
-- album_id     | character varying, foreign key
-- popularity   | integer
-- duration_ms  | integer
-- track_number | integer

DROP TABLE IF EXISTS songs;

CREATE TABLE songs (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    artist_id VARCHAR(50),
    album_id VARCHAR(50),
    popularity INT,
    duration_ms INT,
    track_number INT,
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------

-- Relation Users
-- column_name |          data_type
---------------+-----------------------------
-- hashed_pwd  | bytea
-- created_at  | timestamp without time zone
-- id          | character varying
-- username    | character varying
-- email       | character varying

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    hashed_pwd BYTEA,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------

-- Relation Spotify Users
--    column_name    |     data_type
---------------------+-------------------
-- id                | character varying
-- spotify_username  | character varying
-- spotify_email     | character varying
-- spotify_image_url | character varying
-- spotify_uri       | character varying
-- user_id           | character varying, foreign key

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

