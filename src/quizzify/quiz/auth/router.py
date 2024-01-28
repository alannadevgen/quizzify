import logging
import os
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from quizzify.quiz.utils.helpers import encode_str_to_base64, generate_random_string

# load environment variables
load_dotenv()
# define router for authentication endpoints
router = APIRouter()
# define logger
logger = logging.getLogger(__name__)


SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_TOKEN_URL = os.environ.get("SPOTIFY_TOKEN_URL")
SPOTIFY_AUTH_URL = os.environ.get("SPOTIFY_AUTH_URL")
SPOTIFY_AUTH_SCOPE = os.environ.get("SPOTIFY_AUTH_SCOPE")
STATE = generate_random_string(16)


@router.get(
    path="/login",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
    summary="Redirect user to Spotify Authorization URL",
    description=(
        "The user will be redirected to the Spotify Authorization URL to authorize "
        "the application. After authorization, the user will be redirected to the "
        "callback URL specified in the Spotify Developer Dashboard."
    ),
)
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
    logger.info("Redirecting user to Spotify Authorization URL.")
    authorization_url = (
        SPOTIFY_AUTH_URL
        + "?"
        + urlencode(
            {
                "client_id": SPOTIFY_CLIENT_ID,
                "redirect_uri": SPOTIFY_REDIRECT_URI,
                "response_type": "code",
                "scope": SPOTIFY_AUTH_SCOPE,
                "state": STATE,
                "show_dialog": True,  # ask user to reauthorize if already authorized
            }
        )
    )
    return RedirectResponse(url=authorization_url, status_code=307)


@router.get(
    path="/callback",
    status_code=status.HTTP_302_FOUND,
    summary="Callback URL for Spotify Authorization",
    description=(
        "The user will be redirected to this URL after authorizing the application "
        "on the Spotify Authorization URL. This endpoint will exchange the "
        "authorization code for an access token."
    ),
)
async def callback(
    request: Request,
    code: str,
    state: str = None,
):
    """Redirect user to Spotify Authorization URL.

    The user will be redirected to this URL after authorizing the application
    on the Spotify Authorization URL. This endpoint will exchange the
    authorization code for an access token.

    Parameters
    ----------
    request : Request
        The request object.
    code : str
        The authorization code returned by Spotify.
    state : str, optional
        The state returned by Spotify, by default None

    Returns
    -------
    dict
        A dictionary containing the access token and other token information.
    """
    logger.info("Callback URL for Spotify Authorization")
    # Check if state matches
    if state is not None and state != STATE:
        raise HTTPException(
            status_code=400,
            detail="State not provided",
        )

    if code is None:
        raise HTTPException(
            status_code=400,
            detail="Authorization code not provided",
        )

    # Exchange code for access token
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    # Encode authorization info to base64
    auth_info = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded_auth_info = encode_str_to_base64(auth_info)

    # header for token request
    header_data = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + str(encoded_auth_info),
    }
    response = requests.post(
        url="https://accounts.spotify.com/api/token",
        data=token_data,
        headers=header_data,
    )

    if response.status_code == 200:
        raw_response = response.json()
        access_token = raw_response["access_token"]
        refresh_token = raw_response["refresh_token"]
        token_expiration = raw_response["expires_in"]
        token_expiration_date = datetime.now() + timedelta(seconds=token_expiration)
        scope = raw_response["scope"]
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_expiration": token_expiration,
            "token_expiration_date": token_expiration_date,
            "scope": scope,
        }
        # TODO: Store the token securely (e.g., in a database) for future use
        os.environ["ACCESS_TOKEN"] = access_token
        os.environ["REFRESH_TOKEN"] = refresh_token
        os.environ["TOKEN_EXPIRATION"] = str(token_expiration)
        os.environ["TOKEN_EXPIRATION_DATE"] = str(token_expiration_date)
        os.environ["SCOPE"] = scope
        return tokens
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve access token",
        )


@router.get(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description=("Refresh the access token using the refresh token."),
)
async def refresh_token():
    """Refresh access token.

    Refresh the access token using the refresh token.

    Returns
    -------
    dict
        A dictionary containing the access token and other token information.
    """
    # Check if refresh token is available
    if "REFRESH_TOKEN" not in os.environ:
        raise HTTPException(
            status_code=400,
            detail="Refresh token not available",
        )

    # Exchange code for access token
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": os.environ["REFRESH_TOKEN"],
    }
    # Encode authorization info to base64
    auth_info = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded_auth_info = encode_str_to_base64(auth_info)

    # header for token request
    header_data = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + str(encoded_auth_info),
    }
    response = requests.post(
        url=SPOTIFY_TOKEN_URL,
        data=token_data,
        headers=header_data,
    )

    if response.status_code == 200:
        raw_response = response.json()
        for key, value in raw_response.items():
            print(f"{key}: {value}")
        token_expiration_date = datetime.now() + timedelta(
            seconds=raw_response["expires_in"]
        )
        tokens = {
            "access_token": raw_response["access_token"],
            # "refresh_token": raw_response["refresh_token"],
            "token_expiration": raw_response["expires_in"],
            "token_expiration_date": token_expiration_date,
            "scope": raw_response["scope"],
        }
        return tokens
