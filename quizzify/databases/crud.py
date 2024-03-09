import logging
from uuid import UUID

from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

from quizzify.databases.db_connection import connect_to_db
from quizzify.utils.helpers import flatten_list
from quizzify.utils.schemas import Album, Artist, Song

load_dotenv()
logger = logging.getLogger(__name__)


def create_user(
    user_id: UUID,
    username: str,
    email: str,
    hashed_pwd: str,
):
    """
    Register a user in the quizz and add its information in the database.

    Parameters
    ----------
    user_id : UUID
        The user's unique identifier.
    username : str
        The username for the new account.
    email : str
        The user's email.
    hashed_pwd : str
        The hashed password for the new account.
    """
    # Connect to your PostgreSQL database
    connection = connect_to_db()
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute(
        query=(
            "INSERT INTO users "
            "(user_id, username, email, hashed_pwd) "
            "VALUES"
            "(%(user_id)s, %(username)s, %(email)s, %(hashed_pwd)s );"
        ),
        vars={
            "user_id": str(user_id),
            "username": username,
            "email": email,
            "hashed_pwd": hashed_pwd,
        },
    )
    # Make the changes to the database persistent
    connection.commit()
    logger.info("User successfully created.")

    # Close communication with the database
    cursor.close()
    connection.close()


def create_spotify_user(
    spotify_id: UUID,
    user_id: UUID,
    spotify_username: str,
    spotify_email: str,
    spotify_image_url: str,
    spotify_uri: str,
):
    """Register a user by adding its Spotify information in the database.

    Parameters
    ----------
    spotify_id : UUID
        The user's unique identifier.
    user_id : UUID
        The user's unique identifier.
    spotify_username : str
        The user's Spotify username.
    spotify_email : str
        The user's Spotify email.
    spotify_image_url : str
        The user's Spotify image URL.
    spotify_uri : str
        The user's Spotify URI.
    """
    # Connect to the PostgreSQL database
    connection = connect_to_db()
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute(
        query=(
            "INSERT INTO spotify_users "
            "(spotify_id, user_id, spotify_username, spotify_email, spotify_image_url, "
            "spotify_uri) "
            "VALUES"
            "("
            "%(spotify_id)s, %(user_id)s, %(spotify_username)s, %(spotify_email)s, "
            "%(spotify_image_url)s, %(spotify_uri)s"
            ");"
        ),
        vars={
            "spotify_id": spotify_id,
            "user_id": str(user_id),
            "spotify_username": spotify_username,
            "spotify_email": spotify_email,
            "spotify_image_url": spotify_image_url,
            "spotify_uri": spotify_uri,
        },
    )
    # Make the changes to the database persistent
    connection.commit()
    logger.info("Spotify user successfully created.")

    # Close communication with the database
    cursor.close()
    connection.close()


def get_user_by_email(
    email: str,
):
    """Check if the email is already in use.

    Parameters
    ----------
    email : str
        The user's email.

    Returns
    -------
    tuple
        The user's email and hashed password.
    """
    # Connect to your PostgreSQL database
    connection = connect_to_db()
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute(
        query="SELECT username, email, hashed_pwd FROM users WHERE email = %(email)s;",
        vars={"email": email},
    )
    user_email = cursor.fetchone()
    # Close communication with the database
    cursor.close()
    connection.close()
    return user_email


def get_user_by_username(
    username: str,
):
    """Get a user by its username.

    Parameters
    ----------
    username : str
        The user's username.

    Returns
    -------
    str
        The user's username.
    """
    # Connect to your PostgreSQL database
    connection = connect_to_db()
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute(
        query="SELECT username FROM users WHERE username = %(username)s;",
        vars={"username": username},
    )
    user_email = cursor.fetchone()
    # Close communication with the database
    cursor.close()
    connection.close()
    return user_email


def get_user_by_spotify_id(
    spotify_id: str,
):
    """Get a user by its Spotify ID.

    Parameters
    ----------
    spotify_id : str
        The user's Spotify ID.

    Returns
    -------
    str
        The user's Spotify ID.
    """
    # Connect to your PostgreSQL database
    connection = connect_to_db()
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute(
        query="SELECT spotify_id FROM spotify_users WHERE spotify_id = %(spotify_id)s;",
        vars={"spotify_id": spotify_id},
    )
    user_email = cursor.fetchone()
    # Close communication with the database
    cursor.close()
    connection.close()
    return user_email


def get_random_artist():
    """Get a random artist from the database.

    Returns
    -------
    dict
        A random artist.
    """
    connection = connect_to_db()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        query=(
            "SELECT id, name, popularity, image_url FROM artists OFFSET floor("
            "random() * (SELECT COUNT(*) FROM artists)) LIMIT 1;"
        )
    )
    random_artist = cursor.fetchone()
    cursor.close()
    connection.close()
    return random_artist


def get_random_song():
    """Get a random song from the database.

    Returns
    -------
    dict
        A random song.
    """
    connection = connect_to_db()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        query=(
            "SELECT id, name, artist_id, album_id, popularity, duration_ms, "
            "track_number FROM songs OFFSET floor("
            "random() * (SELECT COUNT(*) FROM songs)) LIMIT 1;"
        )
    )
    random_song = cursor.fetchone()
    cursor.close()
    connection.close()
    return random_song


def get_artists_ids():
    """Get all the artists' IDs from the database.

    Returns
    -------
    list
        A list of all the artists' IDs.
    """
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query="SELECT id FROM artists;")
    artists_ids = cursor.fetchall()
    cursor.close()
    connection.close()
    return flatten_list(artists_ids)


def insert_artist(
    artist: Artist,
):
    """Insert an artist into the database.

    Parameters
    ----------
    artist : Artist
        The artist to insert into the database.
    """
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
        query=(
            "INSERT INTO artists "
            "(id, name, image_url, popularity) "
            "VALUES"
            "(%(artist_id)s, %(artist_name)s, %(artist_image)s, %(popularity)s);"
        ),
        vars={
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image": artist.image_url,
            "popularity": artist.popularity,
        },
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_albums_ids():
    """Get all the albums' IDs from the database.

    Returns
    -------
    list
        A list of all the albums' IDs.
    """
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query="SELECT id FROM albums;")
    albums_ids = cursor.fetchall()
    cursor.close()
    connection.close()
    return flatten_list(albums_ids)


def get_songs_ids():
    """Get all the songs' IDs from the database.

    Returns
    -------
    list
        A list of all the songs' IDs.
    """
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query="SELECT id FROM songs;")
    songs_ids = cursor.fetchall()
    cursor.close()
    connection.close()
    return flatten_list(songs_ids)


def insert_album(
    album: Album,
):
    """Insert an album into the database.

    Parameters
    ----------
    album : Album
        The album to insert into the database.
    """
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
        query=(
            "INSERT INTO albums "
            "(id, name, image_url, release_year, popularity) "
            "VALUES"
            "(%(album_id)s, %(album_name)s, %(album_image)s, %(album_release_year)s, "
            "%(popularity)s);"
        ),
        vars={
            "album_id": album.id,
            "album_name": album.name,
            "album_image": album.image_url,
            "album_release_year": album.release_year,
            "popularity": album.popularity,
        },
    )
    connection.commit()
    cursor.close()
    connection.close()


def insert_song(
    song: Song,
):
    """Insert a song into the database.

    Parameters
    ----------
    song : Song
        The song to insert into the database.
    """
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
        query=(
            "INSERT INTO songs "
            "(id, name, artist_id, album_id, popularity, duration_ms, track_number) "
            "VALUES"
            "(%(song_id)s, %(song_name)s, %(artist_id)s, %(album_id)s, %(popularity)s, "
            "%(duration_ms)s, %(track_number)s);"
        ),
        vars={
            "song_id": song.id,
            "song_name": song.name,
            "artist_id": song.artist_id,
            "album_id": song.album_id,
            "popularity": song.popularity,
            "duration_ms": song.duration_ms,
            "track_number": song.track_number,
        },
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_random_artist_song():
    """Get a random artist and song from the database.

    Returns
    -------
    dict
        A random song and its artist.
    """
    connection = connect_to_db()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        query=(
            "SELECT songs.name AS song_name, artists.name AS artist_name "
            "FROM songs "
            "INNER JOIN artists "
            "ON songs.artist_id = artists.id "
            "OFFSET floor(random() * (SELECT COUNT(*) FROM songs))"
            "LIMIT 1;"
        )
    )
    random_artist_song = cursor.fetchone()
    cursor.close()
    connection.close()
    return random_artist_song
