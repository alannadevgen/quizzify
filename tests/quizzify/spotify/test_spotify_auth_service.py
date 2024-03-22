import os
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from quizzify.spotify.spotify_token_manager import SpotifyTokenManager


@pytest.fixture
def spotify_auth_service():
    # Set up SpotifyTokenManager with mock environment variables
    with patch.dict(
        os.environ,
        {
            "SPOTIFY_CLIENT_ID": os.environ.get("SPOTIFY_CLIENT_ID"),
            "SPOTIFY_CLIENT_SECRET": os.environ.get("SPOTIFY_CLIENT_SECRET"),
            "SPOTIFY_TOKEN_URL": os.environ.get("SPOTIFY_TOKEN_URL"),
            "SPOTIFY_AUTH_URL": os.environ.get("SPOTIFY_AUTH_URL"),
            "SPOTIFY_AUTH_SCOPE": os.environ.get("SPOTIFY_AUTH_SCOPE"),
            "SPOTIFY_REDIRECT_URI": os.environ.get("SPOTIFY_REDIRECT_URI"),
            "STATE": "PUepTCduNgbcyH6Y",
        },
    ):
        yield SpotifyTokenManager()


def test_refresh_token(spotify_auth_service):
    # Mock the requests.post method
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600,  # 1 hour
        }

        # Set the refresh token
        spotify_auth_service.refresh_token = "valid_refresh_token"

        # Call the refresh_access_token method
        spotify_auth_service.refresh_access_token()

        # Check that access token and expiration date are updated
        assert spotify_auth_service.access_token == "new_access_token"
        # set seconds and microseconds to 0 for comparison
        expected_expiration_date = spotify_auth_service.token_expiration_date.replace(
            second=0,
            microsecond=0,
        )
        expiration_date = datetime.now().replace(
            second=0,
            microsecond=0,
        ) + timedelta(seconds=3600)
        assert expected_expiration_date == expiration_date


def test_generate_access_token(spotify_auth_service):
    # Mock the requests.post method
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,  # 1 hour
        }

        # Call the generate_access_token method
        spotify_auth_service.generate_access_token(
            code="valid_code",
            state="PUepTCduNgbcyH6Y",
        )

        # Check that access token, refresh token, and expiration date are updated
        assert spotify_auth_service.access_token == "new_access_token"
        assert spotify_auth_service.refresh_token == "new_refresh_token"
        # set seconds and microseconds to 0 for comparison
        expected_expiration_date = spotify_auth_service.token_expiration_date.replace(
            second=0,
            microsecond=0,
        )
        expiration_date = datetime.now().replace(
            second=0,
            microsecond=0,
        ) + timedelta(seconds=3600)
        assert expected_expiration_date == expiration_date


def test_get_access_token_existing_token_not_expired(spotify_auth_service):
    # Set an existing access token and a future expiration date
    mock_access_token = "existing_access_token"
    mock_token_expiration_date = datetime.now() + timedelta(seconds=3600)

    # Patch the private attribute directly to return the mock_access_token
    with patch.object(
        spotify_auth_service,
        "_SpotifyTokenManager__access_token",
        new=mock_access_token,
    ), patch.object(
        spotify_auth_service,
        "_SpotifyTokenManager__token_expiration_date",
        new=mock_token_expiration_date,
    ):
        # Call the get_access_token method
        result = spotify_auth_service.get_access_token()

        # Check that the existing access token is returned
        assert result["access_token"] == mock_access_token
        assert result["token_expiration_date"] == mock_token_expiration_date


def test_get_access_token_existing_token_expired_refresh_token_available(
    spotify_auth_service,
):
    # Set an expired access token and a refresh token
    spotify_auth_service._SpotifyTokenManager__access_token = "expired_access_token"
    spotify_auth_service._SpotifyTokenManager__token_expiration_date = (
        datetime.now() - timedelta(minutes=10)
    )
    spotify_auth_service._SpotifyTokenManager__refresh_token = "valid_refresh_token"

    # Mock the requests.post method
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600,  # 1 hour
        }

        # Call the get_access_token method
        result = spotify_auth_service.get_access_token()

        # Check that the access token is refreshed and returned
        assert result["access_token"] == "new_access_token"


def test_get_access_token_no_valid_tokens(spotify_auth_service):
    """Check that an error is raised if there is no valid access token or refresh token.

    Call the get_access_token method without valid tokens
    with pytest.raises(ValueError, match="No valid access token or refresh token"):
    """
    # Remove access token and refresh token
    spotify_auth_service._SpotifyTokenManager__access_token = None
    spotify_auth_service._SpotifyTokenManager__refresh_token = None

    # Call the get_access_token method without valid tokens
    with pytest.raises(
        ValueError,
        match="No valid access token or refresh token available",
    ):
        spotify_auth_service.get_access_token()
