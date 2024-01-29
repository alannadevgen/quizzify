import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

from quizzify.quiz.utils.helpers import encode_str_to_base64

load_dotenv()


class SpotifyAuthService:
    """Service for authenticating and authorizing the Spotify API.

    This class handles the authentication and authorization for the Spotify API.
    It also handles the refreshing of the access token.

    Attributes
    ----------
    client_id : str
        The client ID for the Spotify API.
    client_secret : str
        The client secret for the Spotify API.
    token_url : str
        The URL to request an access token from the Spotify API.
    auth_url : str
        The URL to redirect the user to for authorization.
    auth_scope : str
        The scope of authorization for the Spotify API.
    redirect_uri : str
        The redirect URI for the Spotify API.

    Parameters
    ----------
    refresh_token : str
        The refresh token for the Spotify API.
    access_token : str
        The access token for the Spotify API.
    token_expiration_date : datetime

    Methods
    -------
    exchange_code_for_token(code: str, state: str)
        Exchange the authorization code for an access token.
    refresh_access_token()
        Refresh the access token.
    """

    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    token_url = os.environ.get("SPOTIFY_TOKEN_URL")
    auth_url = os.environ.get("SPOTIFY_AUTH_URL")
    auth_scope = os.environ.get("SPOTIFY_AUTH_SCOPE")
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")

    def __init__(self):
        self._refresh_token = None
        self._access_token = None
        self._token_expiration_date = None

    @property
    def refresh_token(self):
        """Return the refresh token for the Spotify API."""
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        """Set the refresh token for the Spotify API."""
        self._refresh_token = value

    @property
    def access_token(self):
        """Return the access token for the Spotify API."""
        return self._access_token

    @property
    def token_expiration_date(self):
        """Return the expiration date of the access token for the Spotify API."""
        return self._token_expiration_date

    @property
    def is_token_expired(self):
        """Check if the access token has expired.

        Returns
        -------
        bool
            True if the access token has expired, False otherwise.
        """
        return datetime.now() > self.token_expiration_date

    def get_access_token(self):
        """Return the access token for the Spotify API.

        Fetches the latest token. If the access token is not expired, it will
        return the access token. If the access token is expired, it will refresh
        the access token and return the new access token.

        Returns
        -------
        str
            The access token for the Spotify API.

        Raises
        ------
        ValueError
            If no valid access token or refresh token is available.
        """
        if self._access_token and not self.is_token_expired:
            return self._access_token
        elif self._refresh_token:
            return self.refresh_access_token()
        else:
            raise ValueError("No valid access token or refresh token available.")

    def generate_access_token(self, code: str, state: str):
        """Exchange the authorization code for an access token.

        Parameters
        ----------
        code : str
            The authorization code from the Spotify API.
        state : str
            The state from the Spotify API.
        """
        # Check if state matches
        current_state = os.environ.get("STATE")
        if state is not None and state != current_state:
            raise ValueError("State not provided")

        if code is None:
            raise ValueError("Authorization code not provided")

        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        auth_info = f"{self.client_id}:{self.client_secret}"
        encoded_auth_info = encode_str_to_base64(auth_info)
        header_data = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + str(encoded_auth_info),
        }
        response = requests.post(
            url=self.token_url,
            data=token_data,
            headers=header_data,
            timeout=120,  # 2 minutes
        )

        if response.status_code == 200:
            raw_response = response.json()
            self._access_token = raw_response["access_token"]
            self._refresh_token = raw_response["refresh_token"]
            token_expiration = raw_response["expires_in"]
            self._token_expiration_date = datetime.now() + timedelta(
                seconds=token_expiration
            )
        else:
            # Handle the error as needed
            raise Exception("Failed to retrieve access token")

    def refresh_access_token(self):
        """Refresh the access token.

        Returns
        -------
        str
            The access token for the Spotify API.

        Raises
        ------
        Exception
            If the refresh token is not available.
        Exception
            If the access token could not be refreshed.
        """
        if not self._refresh_token:
            raise Exception("Refresh token not available")

        token_data = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        auth_info = f"{self.client_id}:{self.client_secret}"
        encoded_auth_info = encode_str_to_base64(auth_info)
        header_data = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + str(encoded_auth_info),
        }
        response = requests.post(
            url=self.token_url,
            data=token_data,
            headers=header_data,
            timeout=120,  # 2 minutes
        )

        if response.status_code == 200:
            raw_response = response.json()
            self._access_token = raw_response["access_token"]
            token_expiration = raw_response["expires_in"]
            self._token_expiration_date = datetime.now() + timedelta(
                seconds=token_expiration
            )
        else:
            raise Exception("Failed to refresh access token")
