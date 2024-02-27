import logging
from uuid import UUID

from dotenv import load_dotenv

from databases.db_connection import connect_to_db

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
