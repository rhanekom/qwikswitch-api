from src.qwikswitchapi.qsapi import QSApi


def test_base_uri_without_trailing_slash_gets_added():
    api = QSApi(base_uri="https://qwikswitch.com/api/v1")
    assert api.base_uri == "https://qwikswitch.com/api/v1/"
