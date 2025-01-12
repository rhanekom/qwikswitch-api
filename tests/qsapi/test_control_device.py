import pytest
import requests

from qwikswitchapi.qs_exception import QSException, QSRequestErrorException, QSRequestFailedException
from qwikswitchapi.utility.url_builder import UrlBuilder


def test_success_returns_control_result(api, mock_request, mock_api_keys):
    device_id = "@112331"
    level = 50
    response = {
        "success": True,
        "device": device_id,
        "level": level
    }

    mock_request.get(UrlBuilder.build_control_url(mock_api_keys.read_write_key, device_id, level), json=response)
    result = api.control_device(mock_api_keys, device_id, level)

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

def test_logical_error_raises_exception(response, api, mock_request, mock_api_keys):
    device = "@112331"
    level = -1
    mock_request.get(UrlBuilder.build_control_url(mock_api_keys.read_write_key, device, level),
                     json=response)

    with pytest.raises(QSRequestErrorException):
        api.control_device(mock_api_keys, device, level)

def test_error_raises_exception(api, mock_request, mock_api_keys):
    device = "@112331"
    level = -1
    mock_request.get(UrlBuilder.build_control_url(mock_api_keys.read_write_key, device, level),
                     exc=requests.exceptions.Timeout)

    with pytest.raises(QSRequestFailedException):
        api.control_device(mock_api_keys, device, level)

def test_with_unknown_error_throws_exception(api, mock_request, mock_api_keys):
    device = "@112331"
    level = -1
    mock_request.get(UrlBuilder.build_control_url(mock_api_keys.read_write_key, device, level), status_code=401)

    with pytest.raises(QSException):
        api.control_device(mock_api_keys, device, level)