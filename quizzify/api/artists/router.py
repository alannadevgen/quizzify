from typing import Dict, List

from fastapi import APIRouter, Header

from quizzify.api.artists import service
from quizzify.utils.schemas import TimeRange

# define router for artists endpoints
router = APIRouter()


@router.post(
    path="/top",
    response_model=List[Dict],
    summary="Return the user's top artists from Spotify",
    description=(
        "Return the user's top artists from Spotify. This endpoint requires an "
        "access token."
    ),
)
async def get_top_artists(
    time_range: TimeRange,
    limit: int,
    user_id: str = Header(),
):
    """Return the user's top artists from Spotify.

    Parameters
    ----------
    time_range : str, optional
        The time range for the top artists, by default "short_term"
    limit : int
        The number of artists to fetch (the maximum is set to 50 by the Spotify API).
    user_id : str
        The user's Spotify ID.

    Returns
    -------
    list
        A list of the user's top artists.
    """
    if limit > 50:
        raise ValueError("Limit cannot exceed 50 artists.")

    top_artists = service.get_top_artists(
        time_range=time_range,
        limit=limit,
    )
    return top_artists


@router.get(
    path="/random",
    # response_model=List[Dict],
    summary="Return random artists from Spotify",
    description="Return random artists from the database.",
)
async def get_random_artist():
    """Return random artists from Spotify.

    Returns
    -------
    list
        A list of random artists.
    """
    random_artist = service.get_random_artist()
    return random_artist
