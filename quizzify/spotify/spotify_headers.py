from fastapi import HTTPException, status

from quizzify.spotify.spotify_token_manager import SpotifyTokenManager

# instantiate token manager for Spotify access token
spotify_auth = SpotifyTokenManager()


def spotify_headers():
    """Return the headers for the Spotify API.

    Returns
    -------
    dict
        The headers for the Spotify API.
    """
    global spotify_auth
    access_token = spotify_auth.access_token

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing access token",
        )

    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
