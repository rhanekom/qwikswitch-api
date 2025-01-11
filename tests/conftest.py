import pytest
import requests_mock

from src.qwikswitchapi.entities.apikeys import ApiKeys
from src.qwikswitchapi.qsapi import QSApi


@pytest.fixture
def mock_request():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture()
def mock_api_keys():
    return ApiKeys('read_key', 'read_write_key')

@pytest.fixture()
def api():
    return QSApi()