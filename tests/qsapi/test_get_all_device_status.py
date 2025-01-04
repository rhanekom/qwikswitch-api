import pytest

from src.qwikswitchapi.qs_api import QSApi
from src.qwikswitchapi.qs_exception import QSException
from src.qwikswitchapi.utility.url_builder import UrlBuilder


def test_with_valid_credentials_returns_device_statuses(mock_request, mock_api_keys):
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
            "type": "RELAY QS-D-S5",
            "hardware": "0x81",
            "firmware": "v3.3",
            "epoch": "1736018046",
            "rssi": "58%",
            "value": 0
        }
    }

    mock_request.get(UrlBuilder.build_get_all_device_status_url(mock_api_keys.read_write_key), json=response)

    api = QSApi('email', 'master_key')
    devices = api.get_all_device_status(mock_api_keys)

    assert devices is not None
    assert devices.statuses is not None
    assert len(devices.statuses) == 2
    assert devices.statuses[0].device_id == "@11111a"
    assert devices.statuses[1].device_id == "@11111b"
    assert devices.statuses[0].rssi == 59
    assert devices.statuses[1].rssi == 58

def test_with_unknown_error_throws_exception(mock_request, mock_api_keys):
    mock_request.get(UrlBuilder.build_get_all_device_status_url(mock_api_keys.read_write_key), status_code=401)

    api = QSApi('email', 'master_key')

    with pytest.raises(QSException):
        api.get_all_device_status(mock_api_keys)
