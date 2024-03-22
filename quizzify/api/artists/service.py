import os

from dotenv import load_dotenv

from quizzify.databases import crud
from quizzify.spotify.spotify_requests import spotify_get_user_top_artists
from quizzify.utils.schemas import Artist, TimeRange

# load environment variables
load_dotenv()
# define base URL for Spotify API
SPOTIFY_BASE_URL = os.environ.get("SPOTIFY_BASE_URL")


def get_top_artists(
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
    # get artists IDs from the database
    artists_ids = crud.get_artists_ids()

    # fetch user's top artists from Spotify
    user_top_artists = spotify_get_user_top_artists(
        time_range=time_range,
        limit=limit,
    )

    for artist in user_top_artists:
        current_artist_id = artist["id"]
        if current_artist_id not in artists_ids:
            # add current artist to the list of artists in the database
            artists_ids.append(current_artist_id)
            crud.insert_artist(artist=Artist(**artist))

    return user_top_artists


def get_random_artist():
    """Get random artists from the database.

    Returns
    -------
    list
        A list of random artists.
    """
    random_artist = crud.get_random_artist()
    return random_artist
