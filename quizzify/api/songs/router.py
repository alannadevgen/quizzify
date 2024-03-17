import os
from typing import Annotated, Dict, List

from fastapi import APIRouter, Header

from quizzify.api.songs import service
from quizzify.utils.schemas import TimeRange

# define router for songs endpoints
router = APIRouter()


@router.post(
    path="/top",
    response_model=List[Dict],
    summary="Return the user's top songs from Spotify",
    description=(
        "Return the user's top songs from Spotify. This endpoint requires an "
        "access token."
    ),
)
async def get_top_songs(
    time_range: TimeRange,
    limit: int,
    user_id: Annotated[str | None, Header()] = os.getenv("SPOTIFY_USER_ID"),
):
    """Return the user's top songs from Spotify.

    Parameters
    ----------
    time_range : str, optional
        The time range for the top songs, by default "short_term"
    limit : int
        The number of songs to fetch (the maximum is set to 50 by the Spotify API).
    user_id : str
        The user's Spotify ID.

    Returns
    -------
    list
        A list of the user's top songs.
    """
    if limit > 50:
        raise ValueError("Limit cannot exceed 50 songs.")

    top_songs = service.get_top_songs(
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
    random_song = service.get_random_song()
    return random_song
