import logging
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from quizzify.quiz.auth import service

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
async def login():
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
    authorization_url = await service.login_redirect_url()
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
    state: str,
):
    """Redirect user to Spotify Authorization URL.

    The user will be redirected to the Spotify Authorization URL to authorize
    the application. After authorization, the user will be redirected to the
    callback URL specified in the Spotify Developer Dashboard.

    Parameters
    ----------
    request : Request
        The request object.
    code : str
        The authorization code returned by Spotify.
    state : str
        The state returned by Spotify.
    """
    logger.info("Callback URL for Spotify Authorization")
    tokens = await service.generate_access_token(code, state)
    return tokens


@router.get(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description=(
        "Refresh the access token using the refresh token. The refresh token expires "
        "after 1 hour, thus the access token must be refreshed every hour."
    ),
)
async def refresh_token():
    """Refresh access token.

    Refresh the access token using the refresh token.

    Returns
    -------
    dict
        A dictionary containing the access token and other token information.
    """
    tokens = await service.refresh_access_token()
    return tokens


@router.get(
    path="/token",
    status_code=status.HTTP_200_OK,
    summary="Get access token",
    description=("Get the access token for the Spotify API."),
)
async def get_token():
    """Get access token.

    Get the access token for the Spotify API.

    Returns
    -------
    dict
        A dictionary containing the access token and other token information.
    """
    tokens = await service.get_token()
    return tokens
