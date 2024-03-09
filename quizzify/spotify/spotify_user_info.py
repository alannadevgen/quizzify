import logging
import os

import requests  # type: ignore[import-untyped]
from dotenv import load_dotenv
from fastapi import HTTPException, status

from quizzify.spotify.spotify_token_manager import SpotifyTokenManager

# load environment variables
load_dotenv()
# define base URL for Spotify API
SPOTIFY_BASE_URL = os.environ.get("SPOTIFY_BASE_URL")
# instantiate token manager for Spotify access token
spotify_auth = SpotifyTokenManager()

logger = logging.getLogger(__name__)


def get_spotify_user_info():
    """Get the user's information from Spotify.

    Returns
    -------
    dict
        The user's information from Spotify.
    """
    global spotify_auth
    access_token = spotify_auth.access_token

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing access token",
        )

    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = f"{SPOTIFY_BASE_URL}/me/"
    response = requests.get(
        api_url,
        headers=headers,
        timeout=120,
    )

    if response.status_code == 200:
        raw_user_info = response.json()
        user_info = {
            "spotify_id": raw_user_info["id"],
            "spotify_name": raw_user_info["display_name"],
            "spotify_email": raw_user_info["email"],
            "image_url": raw_user_info["images"][-1]["url"],
            "country": raw_user_info["country"],
            "spotify_uri": raw_user_info["uri"],
        }
        return user_info
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve user information",
        )
