from fastapi import APIRouter

from quizzify.api.spotify.spotify_requests import spotify_get_user_id
from quizzify.routers.v1.albums import service

router = APIRouter()


@router.get(
    path="/top",
    summary="Return top albums for the current user",
    description="Return top albums from the database.",
)
async def get_top_albums():
    """
    Fetch top albums from user's listening top songs or artists.

    Returns
    -------
    list
        Top albums from user's albums.
    """
    user_id = spotify_get_user_id()
    top_albums = service.get_top_albums(user_id=user_id)
    return top_albums


@router.get(
    path="/random",
    summary="Return a random album from Spotify",
    description="Return random album from the database.",
)
async def get_random_album():
    """
    Fetch a random album from user's listening top songs or artists.

    Returns
    -------
    list
        A random album from user's albums.
    """
    user_id = spotify_get_user_id()
    random_album = service.get_random_album(user_id=user_id)
    return random_album
