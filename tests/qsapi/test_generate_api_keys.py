import pytest
import requests.exceptions

from qwikswitchapi.qs_client import QSClient
from qwikswitchapi.qs_exception import QSException, QSAuthException, QSRequestErrorException, QSRequestFailedException
from qwikswitchapi.utility.url_builder import UrlBuilder


def test_with_valid_credentials_returns_keys(api_client, mock_request):
    response = {
        "ok": 1,
        "r": "aaaa-bbbb-cccc-dddd",
        "rw": "1111-2222-3333-4444"
    }

    mock_request.post(UrlBuilder.build_generate_api_keys_url(), json=response)
    keys = api_client.generate_api_keys()

    assert mock_request.called
    assert keys is not None
    assert keys.read_key == response['r']
    assert keys.read_write_key == response['rw']

def test_with_logical_error_throws_exception(api_client, mock_request):
    response = {
        "ok": 0,
        "err": "Please provide a valid serial key and email address of the registered owner."
    }

    mock_request.post(UrlBuilder.build_generate_api_keys_url(), json=response)

    with pytest.raises(QSAuthException):
        api_client.generate_api_keys()

def test_with_error_throws_exception(api_client, mock_request):
    mock_request.post(UrlBuilder.build_generate_api_keys_url(), exc=requests.exceptions.Timeout)

    with pytest.raises(QSRequestFailedException):
        api_client.generate_api_keys()

def test_with_unknown_error_throws_exception(api_client, mock_request):
    response = {
        "ok": 0
    }

    mock_request.post(UrlBuilder.build_generate_api_keys_url(), json=response)

    with pytest.raises(QSAuthException):
        api_client.generate_api_keys()

def test_with_invalid_credentials_unknown_error_throws_exception(api_client, mock_request):
    mock_request.post(UrlBuilder.build_generate_api_keys_url(), status_code=401)

    with pytest.raises(QSException):
        api_client.generate_api_keys()

def test_method_is_authenticated_on_request(api_client, mock_request):


    @QSClient._ensure_authenticated
    def needs_authentication(self):
        pass

    api_client.needs_authentication = needs_authentication

    response = {
        "ok": 1,
        "r": "aaaa-bbbb-cccc-dddd",
        "rw": "1111-2222-3333-4444"
    }

    mock_request.post(UrlBuilder.build_generate_api_keys_url(), json=response)
    needs_authentication(api_client)

    assert mock_request.called