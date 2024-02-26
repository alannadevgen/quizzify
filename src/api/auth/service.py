import os
import uuid
from urllib.parse import urlencode

import bcrypt
from dotenv import load_dotenv

from databases import crud
from spotify.spotify_auth_service import SpotifyAuthService
from utils.helpers import check_email, generate_random_string

load_dotenv()

# load environment variables
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_AUTH_URL = os.environ.get("SPOTIFY_AUTH_URL")
SPOTIFY_AUTH_SCOPE = os.environ.get("SPOTIFY_AUTH_SCOPE")
SPOTIFY_TOKEN_URL = os.environ.get("SPOTIFY_TOKEN_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")


# instantiate token manager for Spotify access token
spotify_auth = SpotifyAuthService()


async def login_redirect_url():
    """Generate the redirect URL for Spotify Authorization.

    Returns
    -------
    str
        The redirect URL for Spotify Authorization.
    """
    # generate random state
    state = generate_random_string(16)
    # save state to environment variable
    os.environ["STATE"] = state
    # generate authorization URL
    authorization_url = (
        SPOTIFY_AUTH_URL
        + "?"
        + urlencode(
            {
                "client_id": SPOTIFY_CLIENT_ID,
                "redirect_uri": SPOTIFY_REDIRECT_URI,
                "response_type": "code",
                "scope": SPOTIFY_AUTH_SCOPE,
                "state": state,
                "show_dialog": True,  # ask user to reauthorize if already authorized
            }
        )
    )
    return authorization_url


async def generate_access_token(
    code: str,
    state: str,
):
    """Exchange the authorization code for an access token.

    Parameters
    ----------
    code : str
        The authorization code returned from Spotify Authorization.
    state : str
        The state returned from Spotify Authorization.

    Returns
    -------
    dict
        A dictionary containing the access token, refresh token, and token
        expiration date.
    """
    global spotify_auth
    spotify_auth.generate_access_token(code, state)
    return spotify_auth.to_dict()


async def refresh_access_token():
    """Refresh the access token.

    Returns
    -------
    dict
        A dictionary containing the access token, refresh token, and token
        expiration date.
    """
    global spotify_auth
    spotify_auth.refresh_access_token()
    return spotify_auth.to_dict()


async def get_token():
    """Get the latest access token.

    Returns
    -------
    str
        The newest access token.
    """
    global spotify_auth
    return spotify_auth.get_access_token()


async def register_user(
    username: str,
    email: str,
    password: str,
):
    """Register a user in the quizz and add its information in the database.

    Parameters
    ----------
    username : str
        The username for the new account.
    email : str
        The user's email.
    password : str
        The hashed password for the new account.
    """
    user_id = uuid.uuid4()

    # Check if the email is valid
    if not check_email(email):
        raise ValueError("Invalid email")

    # Hash the password
    # Generate a salt (typically a random value)
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # # Verify the hashed password
    # if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
    #     print("Password matches")
    # else:
    #     print("Password does not match")

    # TODO: Check that the username and email are not already in use
    crud.register_user(
        user_id=user_id,
        username=username,
        email=email,
        hashed_pwd=str(hashed_password.decode("utf-8")),
    )
