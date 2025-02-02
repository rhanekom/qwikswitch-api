"""Base Tests for the QSClient class."""

from qwikswitchapi.client import QSClient


def test_base_uri_without_trailing_slash_gets_added():
    api = QSClient("email", "master", base_uri="https://qwikswitch.com/api/v1")
    assert api.base_uri == "https://qwikswitch.com/api/v1/"
