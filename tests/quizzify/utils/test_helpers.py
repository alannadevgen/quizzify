from quizzify.utils.helpers import encode_str_to_base64


def test_encode_str_to_base64():
    """Test encode_str_to_base64() helper function."""
    string_to_encode = "test"
    encoded_string = encode_str_to_base64(string_to_encode)
    assert isinstance(encoded_string, str)
    assert encoded_string == "dGVzdA=="
    assert string_to_encode != encoded_string
