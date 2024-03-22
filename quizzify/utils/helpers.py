import base64
import secrets
from typing import Dict, List, Optional

from email_validator import EmailNotValidError, validate_email


def generate_random_string(
    length: int,
) -> str:
    """Generate a random string of the specified length.

    Parameters
    ----------
    length : int
        The length of the random string to generate.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_string = "".join(secrets.choice(alphabet) for _ in range(length))
    return random_string


def encode_str_to_base64(
    string_to_encode: str,
) -> str:
    """
    Encode a string to base64.

    Parameters
    ----------
    string_to_encode : str
        The string to encode.

    Returns
    -------
    str
        The encoded string.
    """
    string_bytes = string_to_encode.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    encoded_base64_string = base64_bytes.decode("ascii")
    return encoded_base64_string


def flatten_list(matrix: list) -> list:
    """Flatten a matrix using list comprehension.

    Parameters
    ----------
    matrix : list
        The matrix to flatten.

    Returns
    -------
    list
        The flattened matrix.
    """
    return [item for row in matrix for item in row]


def check_email(email: str) -> bool:
    """Check if the email is valid.

    Parameters
    ----------
    email : str
        The email to check.

    Returns
    -------
    bool
        True if the email is valid, False otherwise.
    """
    try:
        # Check that the email address is valid. Turn on check_deliverability
        # for first-time validations like on account creation pages (but not
        # login pages).
        email_info = validate_email(email, check_deliverability=False)

        # After this point, use only the normalized form of the email address,
        # especially before going to a database query.
        email = email_info.normalized

        return True

    except EmailNotValidError:
        # The exception message is human-readable explanation of why it's
        # not a valid (or deliverable) email address.
        return False


def get_highest_resolution_image(images: List[Dict]) -> Optional[Dict[str, str]]:
    """Get the highest resolution image from a list of images (dict).

    Parameters
    ----------
    images : list
        A list of images (dict) containing images with their URL, weight and height.

    Returns
    -------
    highest_resolution_image : dict
        The highest resolution image from the list (URL, weight and height).
    """
    highest_resolution_image = None
    highest_resolution = 0

    for image in images:
        current_resolution = image["height"] * image["width"]
        if current_resolution > highest_resolution:
            highest_resolution = current_resolution
            highest_resolution_image = image

    return highest_resolution_image
