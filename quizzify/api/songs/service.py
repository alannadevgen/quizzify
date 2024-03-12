import logging
import os

import requests  # type: ignore[import-untyped]
from dotenv import load_dotenv
from fastapi import HTTPException

from quizzify.databases import crud
from quizzify.spotify.spotify_headers import spotify_headers
from quizzify.spotify.spotify_requests import spotify_get_album, spotify_get_artist
from quizzify.utils.schemas import Album, Artist, Song, TimeRange

# load environment variables
load_dotenv()
# define base URL for Spotify API
SPOTIFY_BASE_URL = os.environ.get("SPOTIFY_BASE_URL")

logger = logging.getLogger(__name__)


def get_top_songs(
    time_range: TimeRange,
    limit: int,
):
    """Get the user's top songs from Spotify.

    Parameters
    ----------
    time_range : TimeRange
        The time range for the top songs.
    limit : int
        The number of songs to fetch (the maximum is set to 50 by the Spotify API).

    Returns
    -------
    list
        A list of the user's top songs.
    """
    headers = spotify_headers()
    api_url = (
        f"{SPOTIFY_BASE_URL}/me/top/tracks?time_range={time_range.value}&limit={limit}"
    )
    response = requests.get(
        api_url,
        headers=headers,
        timeout=120,
    )

    if response.status_code == 200:
        raw_top_songs = response.json()["items"]
        top_songs = []

        # get artists and songs IDs from the database
        albums_ids = crud.get_albums_ids()
        artists_ids = crud.get_artists_ids()
        song_ids = crud.get_songs_ids()

        for song in range(len(raw_top_songs)):
            for artist in range(len(raw_top_songs[song]["artists"])):
                # insert artist into database
                current_artist_id = raw_top_songs[song]["artists"][artist]["id"]
                if current_artist_id not in artists_ids:
                    # add artist ID to the list of artists already known
                    artists_ids.append(current_artist_id)
                    artist_info = spotify_get_artist(current_artist_id)
                    crud.insert_artist(
                        artist=Artist.model_validate(artist_info),
                    )

                # get artist details
                artists_info = [
                    {"id": artist["id"], "name": artist["name"]}
                    for artist in raw_top_songs[song]["artists"]
                ]

                # get album details
                current_album_id = raw_top_songs[song]["album"]["id"]
                # insert album into database if it is not already there
                if current_album_id not in albums_ids:
                    albums_ids.append(current_album_id)

                    # get album details
                    album_info = spotify_get_album(current_album_id)
                    # insert album info
                    crud.insert_album(
                        album=Album.model_validate(album_info),
                        artist_id=current_artist_id,
                    )

                    # insert song info into the database if it is not already there
                    current_song_id = raw_top_songs[song]["id"]
                    # get song details
                    song_info = {
                        "id": current_song_id,
                        "name": raw_top_songs[song]["name"],
                        "popularity": raw_top_songs[song]["popularity"],
                        "duration_ms": raw_top_songs[song]["duration_ms"],
                        # "preview_url": raw_top_songs[song]["preview_url"],
                        "track_number": raw_top_songs[song]["track_number"],
                        "album_id": raw_top_songs[song]["album"]["id"],
                        "artist_id": raw_top_songs[song]["artists"][artist]["id"],
                    }
                    # insert song into database if it is not already there
                    if current_song_id not in song_ids:
                        song_ids.append(current_song_id)
                        crud.insert_song(song=Song.model_validate(song_info))

                    # create a dictionary with the song, artist and album details
                    current_song = {
                        "song": song_info,
                        "artists": artists_info,
                        "album": album_info,
                    }
                    top_songs.append(current_song)

        return top_songs
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve top songs",
        )


def get_random_song():
    """Get random songs from the database.

    Returns
    -------
    list
        A list of random songs.
    """
    random_song = crud.get_random_song()
    return random_song
