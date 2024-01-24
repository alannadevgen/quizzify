import base64
import os
from typing import Optional
from urllib.parse import urlencode

import httpx
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from quiz.utils.helpers import encode_str_to_base64, generate_random_string

load_dotenv()
router = APIRouter()

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_AUTH_URL = os.environ.get("SPOTIFY_AUTH_URL")
SPOTIFY_AUTH_SCOPE = os.environ.get("SPOTIFY_AUTH_SCOPE")

state = generate_random_string(16)


@router.get("/")
def index():
    """Return the API name and description."""
    return {"Quizzify": "Music Quiz API"}


@router.get("/login")
def login():
    """Redirect user to Spotify Authorization URL.

    The user will be redirected to the Spotify Authorization URL to authorize
    the application. After authorization, the user will be redirected to the
    callback URL specified in the Spotify Developer Dashboard.

    Returns
    -------
    RedirectResponse
        A redirect response to the Spotify Authorization URL.
    """
    authorization_url = (
        SPOTIFY_AUTH_URL
        + "?"
        + urlencode(
            {
                "client_id": SPOTIFY_CLIENT_ID,
                "redirect_uri": SPOTIFY_REDIRECT_URI,
                "response_type": "code",
                "scope": SPOTIFY_AUTH_SCOPE,
            }
        )
    )
    return RedirectResponse(url=authorization_url, status_code=302)
