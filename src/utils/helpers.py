import base64
import secrets


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
