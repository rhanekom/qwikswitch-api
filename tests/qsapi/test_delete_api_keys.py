import pytest
import requests

from qwikswitchapi.qs_exception import QSException, QSRequestErrorException, QSRequestFailedException, QSAuthException
from qwikswitchapi.utility.url_builder import UrlBuilder


def test_with_valid_credentials_returns_none(api_client, mock_request):
    response = {
        "ok": 1,
        "r": None,
        "rw": None
    }

    mock_request.post(UrlBuilder.build_delete_api_keys_url(), json=response)
    api_client.delete_api_keys()

def test_with_logical_error_throws_exception(api_client, mock_request):
    response = {
        "ok": 0,
        "err": "Please provide a valid serial key and email address of the registered owner."
    }

    mock_request.post(UrlBuilder.build_delete_api_keys_url(), json=response)

    with pytest.raises(QSAuthException):
        api_client.delete_api_keys()

def test_with_error_throws_exception(api_client, mock_request):
    mock_request.post(UrlBuilder.build_delete_api_keys_url(), exc=requests.exceptions.Timeout)

    with pytest.raises(QSRequestFailedException):
        api_client.delete_api_keys()

def test_with_unknown_error_throws_exception(api_client, mock_request):
    response = {
        "ok": 0
    }

    mock_request.post(UrlBuilder.build_delete_api_keys_url(), json=response)

    with pytest.raises(QSException):
        api_client.delete_api_keys()

def test_with_invalid_credentials_unknown_error_throws_exception(api_client, mock_request):
    mock_request.post(UrlBuilder.build_delete_api_keys_url(), status_code=401)

    with pytest.raises(QSException):
        api_client.delete_api_keys()