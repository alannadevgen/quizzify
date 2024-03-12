from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    """User schema for the quiz app.

    This schema is used to create a new user in the quiz app or login into its account.
    It contains the user's username, email, and password.
    """

    id: Optional[UUID] = None
    username: str
    email: str
    password: str


class Artist(BaseModel):
    """Artist schema for the Spotify API.

    This schema is used to represent an artist and handle its data (for fetching it,
    storing it, creating a question, and so on).
    """

    id: Optional[str] = None
    name: str
    popularity: Optional[int] = None
    genres: Optional[list] = None
    followers: Optional[int] = None
    image_url: Optional[str] = None


class Album(BaseModel):
    """Album schema for the Spotify API.

    This schema is used to represent an album and handle its data (for fetching it,
    storing it, creating a question, and so on).
    """

    id: Optional[str] = None
    name: str
    image_url: Optional[str] = None
    popularity: Optional[int] = None
    release_year: Optional[str] = None
    total_tracks: Optional[int] = None
    artist_id: Optional[str] = None


class Song(BaseModel):
    """Song schema for the Spotify API.

    This schema is used to represent a song and handle its data (for fetching it,
    storing it, creating a question, and so on).
    """

    id: Optional[str] = None
    name: str
    artist_id: str
    album_id: str
    release_year: Optional[str] = None
    image_url: Optional[str] = None
    popularity: Optional[int] = None
    duration_ms: Optional[int] = None
    preview_url: Optional[str] = None
    track_number: Optional[int] = None


class TimeRange(str, Enum):
    """Time range for the Spotify API.

    This enum is used to represent the time range for the Spotify API calls (short term,
    medium term, long term).
    """

    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"
