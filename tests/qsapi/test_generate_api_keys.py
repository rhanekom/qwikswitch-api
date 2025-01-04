import pytest

from src.qwikswitchapi.qs_api import QSApi
from src.qwikswitchapi.qs_exception import QSException
from src.qwikswitchapi.utility.url_builder import UrlBuilder


def test_with_valid_credentials_returns_keys(mock_api):
    response = {
        "ok": 1,
        "r": "aaaa-bbbb-cccc-dddd",
        "rw": "1111-2222-3333-4444"
    }

    mock_api.post(UrlBuilder.build_generate_api_keys_url(), json=response)

    api = QSApi('email', 'master_key')
    keys = api.generate_api_keys()

    assert keys is not None
    assert keys.read_key == response['r']
    assert keys.read_write_key == response['rw']


def test_with_error_throws_exception(mock_api):
    response = {
        "ok": 0,
        "err": "Please provide a valid serial key and email address of the registered owner."
    }

    mock_api.post(UrlBuilder.build_generate_api_keys_url(), json=response)

    api = QSApi('email', 'master_key')

    with pytest.raises(QSException):
        api.generate_api_keys()

def test_with_unknown_error_throws_exception(mock_api):
    response = {
        "ok": 0
    }

    mock_api.post(UrlBuilder.build_generate_api_keys_url(), json=response)

    api = QSApi('email', 'master_key')

    with pytest.raises(QSException):
        api.generate_api_keys()

def test_with_invalid_credentials_unknown_error_throws_exception(mock_api):
    mock_api.post(UrlBuilder.build_generate_api_keys_url(), status_code=401)

    api = QSApi('email', 'master_key')

    with pytest.raises(QSException):
        api.generate_api_keys()