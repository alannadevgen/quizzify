import logging
from uuid import UUID

from dotenv import load_dotenv

from databases.db_connection import connect_to_db

load_dotenv()
logger = logging.getLogger(__name__)


def register_user(
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
            "INSERT INTO users (id, username, email, hashed_pwd) VALUES "
            "(%(user_id)s, %({username})s, %({email})s, %({hashed_pwd})s);"
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
    logger.info("User registered successfully.")

    # Close communication with the database
    cursor.close()
    connection.close()
