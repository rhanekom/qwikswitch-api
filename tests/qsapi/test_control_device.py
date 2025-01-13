import pytest
import requests

from qwikswitchapi.qs_exception import QSRequestErrorException, QSRequestFailedException
from qwikswitchapi.utility.url_builder import UrlBuilder


def test_success_returns_control_result(authenticated_api_client, mock_request):
    device_id = "@112331"
    level = 50
    response = {
        "success": True,
        "device": device_id,
        "level": level
    }

    mock_request.get(UrlBuilder.build_control_url(authenticated_api_client._api_keys.read_write_key, device_id, level), json=response)
    result = authenticated_api_client.control_device(device_id, level)

    assert result is not None
    assert result.device_id == device_id
    assert result.level == level

@pytest.mark.parametrize("response", [
    {
        "error": "INVALID LEVEL"
    },
    {
        "error": "INVALID DEVICE ID"
    },
    {
        "success": False
    }
])

def test_logical_error_raises_exception(response, authenticated_api_client, mock_request):
    device = "@112331"
    level = -1
    mock_request.get(UrlBuilder.build_control_url(authenticated_api_client._api_keys.read_write_key, device, level),
                     json=response)

    with pytest.raises(QSRequestErrorException):
        authenticated_api_client.control_device(device, level)

def test_error_raises_exception(authenticated_api_client, mock_request):
    device = "@112331"
    level = -1
    mock_request.get(UrlBuilder.build_control_url(authenticated_api_client._api_keys.read_write_key, device, level),
                     exc=requests.exceptions.Timeout)

    with pytest.raises(QSRequestFailedException):
        authenticated_api_client.control_device(device, level)

def test_with_unknown_error_throws_exception(authenticated_api_client, mock_request):
    device = "@112331"
    level = -1
    mock_request.get(UrlBuilder.build_control_url(authenticated_api_client._api_keys.read_write_key, device, level), status_code=401)

    with pytest.raises(QSRequestErrorException):
        authenticated_api_client.control_device(device, level)