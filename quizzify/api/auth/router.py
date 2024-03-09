import logging
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from quizzify.api.auth import service
from quizzify.utils import schemas

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
    path="/tokens/refresh",
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
    path="/tokens",
    status_code=status.HTTP_200_OK,
    summary="Get access token",
    description="Get the latest access token for the Spotify API.",
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


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    summary="Create an account for the quiz app",
    description=(
        "Create a new account for quizzify. This will enable the user to login to the "
        "application and access the quiz features."
    ),
)
async def register_user(
    user: schemas.User,
):
    """Create an account for the quiz app.

    Create a new account for quizzify. This will enable the user to log in to the
    application and access the quiz features.

    Parameters
    ----------
    user : schemas.User
        The user information to create the account (username, email, password).

    Returns
    -------
    dict
        A dictionary containing the user's Spotify information.
    """
    logger.info(f"Creating a new account for the user {user.username}.")
    user = await service.register_user(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    return user


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Log in to the quiz app",
    description=(
        "Log in to the quizzify application. The user will be able to connect to the "
        "account previously created."
    ),
)
async def login_user(
    user: schemas.User,
):
    """Log in to the quiz app.

    Log in to the quizzify application. The user will be able to connect to the
    account previously created by checking if the account exists and the password
    is correct.

    Parameters
    ----------
    user : schemas.User
        The user information to log in (email, password).

    Returns
    -------
    dict
        A dictionary containing the user's Spotify information.
    """
    logger.info(f"Logging in to the account for the user {user.email}.")
    user = await service.login_user(
        email=user.email,
        password=user.password,
    )
    return user
