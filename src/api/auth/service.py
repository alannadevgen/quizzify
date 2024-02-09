import os
from urllib.parse import urlencode

from dotenv import load_dotenv

from spotify.spotify_auth_service import SpotifyAuthService
from utils.helpers import generate_random_string

load_dotenv()

# load environment variables
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_AUTH_URL = os.environ.get("SPOTIFY_AUTH_URL")
SPOTIFY_AUTH_SCOPE = os.environ.get("SPOTIFY_AUTH_SCOPE")
SPOTIFY_TOKEN_URL = os.environ.get("SPOTIFY_TOKEN_URL")

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
    """Get the latest access token."""
    global spotify_auth
    return spotify_auth.get_access_token()
