import os

import requests  # type: ignore[import-untyped]
from dotenv import load_dotenv
from fastapi import HTTPException

from quizzify.spotify.spotify_headers import spotify_headers
from quizzify.utils.helpers import get_highest_resolution_image
from quizzify.utils.schemas import TimeRange

# load environment variables
load_dotenv()
# define base URL for Spotify API
SPOTIFY_BASE_URL = os.environ.get("SPOTIFY_BASE_URL")


def spotify_get_user_top_artists(
    time_range: TimeRange,
    limit: int,
):
    """Get the user's top artists from Spotify.

    Parameters
    ----------
    time_range : str
        The time range for the top artists (short_term, medium_term, long_term).
        Valid values: long_term (calculated from several years of data and including all
        new data as it becomes available), medium_term (approximately last 6 months),
        short_term (approximately last 4 weeks).
    limit
        The number of artists to return.

    Returns
    -------
    list
        A list of the user's top artists.
    """
    headers = spotify_headers()
    api_url = (
        f"{SPOTIFY_BASE_URL}/me/top/artists?time_range={time_range.value}&limit={limit}"
    )
    response = requests.get(
        api_url,
        headers=headers,
        timeout=120,
    )

    if response.status_code == 200:
        raw_top_artists = response.json()["items"]
        top_artists = []
        # Loop over artists
        for raw_artist in raw_top_artists:
            # Get artist details
            best_image = get_highest_resolution_image(images=raw_artist["images"])
            current_artist = {
                "id": raw_artist["id"],
                "name": raw_artist["name"],
                "popularity": raw_artist["popularity"],
                "genres": raw_artist["genres"],
                "followers": raw_artist["followers"]["total"],
                "image_url": best_image["url"] if best_image else None,
            }
            # Append artist to list
            top_artists.append(current_artist)
        return top_artists
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve top artists",
        )


def spotify_get_artist(
    artist_id: str,
):
    """Get an artist information from Spotify.

    Connect to https://api.spotify.com/v1/artists/{id} for the artist's information.

    Parameters
    ----------
    artist_id : str
        The Spotify ID for the artist.

    Returns
    -------
    dict
        The artist's information from Spotify.
    """
    headers = spotify_headers()
    api_url = f"{SPOTIFY_BASE_URL}/artists/{artist_id}"
    response = requests.get(
        api_url,
        headers=headers,
        timeout=120,
    )

    if response.status_code == 200:
        raw_artist_info = response.json()
        best_image = get_highest_resolution_image(images=raw_artist_info["images"])
        artist_info = {
            "id": raw_artist_info["id"],
            "name": raw_artist_info["name"],
            "popularity": raw_artist_info["popularity"],
            "genres": raw_artist_info["genres"],
            "followers": raw_artist_info["followers"]["total"],
            "image_url": best_image["url"] if best_image else None,
        }
        return artist_info
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve artist information",
        )


def spotify_get_album(
    album_id: str,
):
    """Get an artist information from Spotify.

    Connect to https://api.spotify.com/v1/albums/{id} for the album's information.

    Parameters
    ----------
    album_id : str
        The Spotify ID for the album.

    Returns
    -------
    album_info : dict
        The album's information from Spotify.
    """
    headers = spotify_headers()
    api_url = f"{SPOTIFY_BASE_URL}/albums/{album_id}"
    response = requests.get(
        api_url,
        headers=headers,
        timeout=120,
    )

    if response.status_code == 200:
        raw_album_info = response.json()
        # songs_name = [track["name"] for track in raw_album_info["tracks"]["items"]]
        best_image = get_highest_resolution_image(images=raw_album_info["images"])
        album_info = {
            "id": raw_album_info["id"],
            "name": raw_album_info["name"],
            "popularity": raw_album_info.get("popularity"),
            "release_year": raw_album_info["release_date"][:4],
            "total_tracks": raw_album_info["total_tracks"],
            "image_url": best_image["url"] if best_image else None,
        }
        return album_info
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve the album's information",
        )
