import pytest
import requests.exceptions

from qwikswitchapi.constants import DeviceClass
from qwikswitchapi.exceptions import QSRequestErrorException, QSRequestFailedException
from qwikswitchapi.utility import UrlBuilder


def test_with_valid_credentials_returns_device_statuses(authenticated_api_client, mock_request):
    response = {
    "success": True,
        "@11111a": {
            "type": "RELAY QS-D-S5",
            "hardware": "0x81",
            "firmware": "v3.3",
            "epoch": "1736018165",
            "rssi": "59%",
            "value": 0
        },
        "@11111b": {
            "type": "RELAY QS-Q-S9",
            "hardware": "0x81",
            "firmware": "v3.3",
            "epoch": "1736018046",
            "rssi": "58%",
            "value": 0
        }
    }

    mock_request.get(UrlBuilder.build_get_all_device_status_url(authenticated_api_client._api_keys.read_write_key), json=response)

    devices = authenticated_api_client.get_all_device_status()

    assert mock_request.called
    assert devices is not None
    assert devices.statuses is not None
    assert len(devices.statuses) == 2
    assert devices.statuses[0].device_id == "@11111a"
    assert devices.statuses[1].device_id == "@11111b"

    assert devices.statuses[0].rssi == 59
    assert devices.statuses[1].rssi == 58

    assert devices.statuses[0].device_class == DeviceClass.dimmer
    assert devices.statuses[1].device_class == DeviceClass.unknown


def test_with_unknown_error_throws_exception(authenticated_api_client, mock_request):
    mock_request.get(UrlBuilder.build_get_all_device_status_url(authenticated_api_client._api_keys.read_write_key), status_code=401)

    with pytest.raises(QSRequestErrorException):
        authenticated_api_client.get_all_device_status()

@pytest.mark.parametrize("response", [
    {
        "error": "INVALID_API_KEY"
    },
    {
        "success": False
    }
])

def test_logical_error_raises_exception(response, authenticated_api_client, mock_request):
    mock_request.get(UrlBuilder.build_get_all_device_status_url(authenticated_api_client._api_keys.read_write_key),
                     json=response)

    with pytest.raises(QSRequestErrorException):
        authenticated_api_client.get_all_device_status()

def test_error_raises_exception(authenticated_api_client, mock_request):
    mock_request.get(UrlBuilder.build_get_all_device_status_url(authenticated_api_client._api_keys.read_write_key),
                     exc=requests.exceptions.Timeout)

    with pytest.raises(QSRequestFailedException):
        authenticated_api_client.get_all_device_status()