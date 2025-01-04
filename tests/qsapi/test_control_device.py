import pytest

from src.qwikswitchapi.qs_api import QSApi
from src.qwikswitchapi.qs_exception import QSException
from src.qwikswitchapi.utility.url_builder import UrlBuilder


def test_success_returns_control_result(mock_api, mock_api_keys):
    device_id = "@112331"
    level = 50
    response = {
        "success": True,
        "device": device_id,
        "level": level
    }

    mock_api.get(UrlBuilder.build_control_url(mock_api_keys.read_write_key, device_id, level), json=response)
    api = QSApi('email', 'master_key')
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

def test__error_raises_exception(response, mock_api, mock_api_keys):
    device = "@112331"
    level = -1
    mock_api.get(UrlBuilder.build_control_url(mock_api_keys.read_write_key, device, level),
                 json=response)

    api = QSApi('email', 'master_key')

    with pytest.raises(QSException):
        api.control_device(mock_api_keys, device, level)

