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
def api_client():
    return QSClient('email', 'master')

@pytest.fixture()
def authenticated_api_client(mock_api_keys):
    client = QSClient('email', 'master')
    client._api_keys = mock_api_keys
    return client