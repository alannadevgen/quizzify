from typing import Dict, List

from fastapi import APIRouter

from quizzify.api.spotify.spotify_requests import spotify_get_user_id
from quizzify.routers.v1.xsongs import service
from quizzify.utils.schemas import TimeRange

# define router for songs endpoints
router = APIRouter()


@router.get(
    path="/top",
    response_model=List[Dict],
    summary="Return the user's top songs from Spotify",
    description=(
        "Return the user's top songs from Spotify. This endpoint requires an "
        "access token."
    ),
)
async def get_top_songs():
    """Return the user's top songs from Spotify.

    Returns
    -------
    list
        A list of the user's top songs.
    """
    user_id = spotify_get_user_id()
    top_songs = service.get_top_songs(user_id=user_id)
    return top_songs


@router.post(
    path="/top",
    response_model=List[Dict],
    summary="Return the user's top songs from Spotify",
    description=(
        "Return the user's top songs from Spotify. This endpoint requires an "
        "access token."
    ),
)
async def post_top_songs(
    time_range: TimeRange,
    limit: int = 10,
):
    """Return the user's top songs from Spotify.

    Parameters
    ----------
    time_range : str, optional
        The time range for the top songs, by default "short_term"
    limit : int
        The number of songs to fetch (the maximum is set to 50 by the Spotify API).

    Returns
    -------
    list
        A list of the user's top songs.
    """
    if limit > 50:
        raise ValueError("Limit cannot exceed 50 songs.")

    top_songs = service.insert_top_songs(
        time_range=time_range,
        limit=limit,
    )
    return top_songs


@router.get(
    path="/random",
    # response_model=List[Dict],
    summary="Return random songs from Spotify",
    description="Return random songs from the database.",
)
async def get_random_song():
    """Return random songs from Spotify.

    Returns
    -------
    list
        A list of random songs.
    """
    user_id = spotify_get_user_id()
    random_song = service.get_random_song(user_id=user_id)
    return random_song
