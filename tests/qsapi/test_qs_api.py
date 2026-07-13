"""Base Tests for the QSClient class."""

from qwikswitchapi.client import QSClient


def test_base_uri_without_trailing_slash_gets_added():
    api = QSClient("email", "master", base_uri="https://qwikswitch.com/api/v1")
    assert api.base_uri == "https://qwikswitch.com/api/v1/"


def test_api_keys_defaults_to_none_and_is_readable(mock_api_keys):
    api = QSClient("email", "master")
    assert api.api_keys is None

    api.api_keys = mock_api_keys
    assert api.api_keys is mock_api_keys
