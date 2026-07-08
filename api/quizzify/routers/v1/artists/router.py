from typing import Dict, List

from fastapi import APIRouter

from quizzify.api.spotify.spotify_requests import spotify_get_user_id
from quizzify.routers.v1.artists import service
from quizzify.utils.schemas import TimeRange

# define router for artists endpoints
router = APIRouter()


@router.get(
    path="/top",
    summary="Return the user's top artists from Spotify",
    description=(
        "Return the user's top artists from Spotify. "
        "This endpoint requires an access token."
    ),
)
async def get_top_artists():
    """Return the user's top artists from Spotify.

    Returns
    -------
    list
        A list of the user's top artists.
    """
    user_id = spotify_get_user_id()
    top_artists = service.get_top_artists(user_id=user_id)
    return top_artists


@router.get(
    path="/random",
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
    user_id = spotify_get_user_id()
    random_artist = service.get_random_artist(user_id=user_id)
    return random_artist


@router.post(
    path="/top",
    response_model=List[Dict],
    summary="Return the user's top artists from Spotify",
    description=(
        "Return the user's top artists from Spotify. This endpoint requires an "
        "access token."
    ),
)
async def post_top_artists(
    time_range: TimeRange,
    limit: int = 10,
):
    """Return the user's top artists from Spotify.

    Parameters
    ----------
    time_range : str, optional
        The time range for the top artists. Valid values are 'short_term',
        'medium_term' and 'long_term'.
    limit : int
        The number of artists to fetch (the maximum is set to 50 by the Spotify API).

    Returns
    -------
    list
        A list of the user's top artists.
    """
    if limit > 50:
        raise ValueError("Limit cannot exceed 50 artists.")

    top_artists = service.insert_top_artists(
        time_range=time_range,
        limit=limit,
    )
    return top_artists
