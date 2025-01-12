import pytest
import requests.exceptions

from qwikswitchapi.constants import Constants
from qwikswitchapi.qs_exception import QSException
from qwikswitchapi.utility.url_builder import UrlBuilder


def test_with_valid_credentials_returns_device_statuses(api, mock_request, mock_api_keys):
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

    mock_request.get(UrlBuilder.build_get_all_device_status_url(mock_api_keys.read_write_key), json=response)

    devices = api.get_all_device_status(mock_api_keys)

    assert devices is not None
    assert devices.statuses is not None
    assert len(devices.statuses) == 2
    assert devices.statuses[0].device_id == "@11111a"
    assert devices.statuses[1].device_id == "@11111b"

    assert devices.statuses[0].rssi == 59
    assert devices.statuses[1].rssi == 58

    assert devices.statuses[0].device_class == Constants.DeviceClass.dimmer
    assert devices.statuses[1].device_class == Constants.DeviceClass.unknown


def test_with_unknown_error_throws_exception(api, mock_request, mock_api_keys):
    mock_request.get(UrlBuilder.build_get_all_device_status_url(mock_api_keys.read_write_key), status_code=401)

    with pytest.raises(QSException):
        api.get_all_device_status(mock_api_keys)

@pytest.mark.parametrize("response", [
    {
        "error": "INVALID_API_KEY"
    },
    {
        "success": False
    }
])

def test_logical_error_raises_exception(response, api, mock_request, mock_api_keys):
    mock_request.get(UrlBuilder.build_get_all_device_status_url(mock_api_keys.read_write_key),
                     json=response)

    with pytest.raises(QSException):
        api.get_all_device_status(mock_api_keys)

def test_error_raises_exception(api, mock_request, mock_api_keys):
    mock_request.get(UrlBuilder.build_get_all_device_status_url(mock_api_keys.read_write_key),
                     exc=requests.exceptions.Timeout)

    with pytest.raises(QSException):
        api.get_all_device_status(mock_api_keys)