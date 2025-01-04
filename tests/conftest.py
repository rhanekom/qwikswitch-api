import pytest
import requests_mock

from src.qwikswitchapi.entities.api_keys import ApiKeys


@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture()
def mock_api_keys():
    return ApiKeys('read_key', 'read_write_key')
