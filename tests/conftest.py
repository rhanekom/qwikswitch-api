import pytest
import requests_mock

from qwikswitchapi.entities.api_keys import ApiKeys
from qwikswitchapi.qs_client import QSClient


@pytest.fixture
def mock_request():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture()
def mock_api_keys():
    return ApiKeys('read_key', 'read_write_key')

@pytest.fixture()
def api():
    return QSClient()