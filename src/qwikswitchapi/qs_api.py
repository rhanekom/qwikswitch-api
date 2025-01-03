from urllib.parse import urljoin, quote_plus

import requests
from requests.exceptions import RequestException

from src.qwikswitchapi.api_keys import ApiKeys
from src.qwikswitchapi.control_result import ControlResult
from src.qwikswitchapi.qs_exception import QSException

class QSApi:
    DEFAULT_BASE_URI = 'https://qwikswitch.com/api/v1/'

    def __init__(self, email:str, master_key:str, base_uri:str=DEFAULT_BASE_URI):
        self._email = email
        self._master_key = master_key
        self._base_uri = base_uri

    def generate_api_keys(self) -> ApiKeys:
        url = urljoin(self._base_uri, 'keys')
        req = {
            'email': self._email,
            'master_key': self._master_key
        }

        try:
            resp = requests.post(url, json=req)
            json_resp = QSApi._parse_response(resp)
            return ApiKeys.from_json(json_resp)
        except RequestException as ex:
            QSApi._raise_request_failure(url, ex)

    def control_device(self, auth:ApiKeys, device_id:str, level:int):
        url = QSApi._build_control_url(self._base_uri, auth.read_write_key, device_id, level)

        try:
            resp = requests.get(url)
            json_resp = QSApi._parse_response(resp)
            return ControlResult.from_json(json_resp)
        except RequestException as ex:
            QSApi._raise_request_failure(url, ex)

    @staticmethod
    def _parse_response(resp) -> dict:
        if resp.status_code != 200:
            QSApi._raise_request_error(resp)

        json_resp = resp.json()

        if 'err' in json_resp:
            QSApi._raise_request_error(resp)
        if 'ok' in json_resp and json_resp['ok'] == 0:
            QSApi._raise_request_error(resp)
        if 'success' in json_resp and not json_resp['success']:
            QSApi._raise_request_error(resp)
        if 'error' in json_resp and "No Data" not in json_resp['error']:
            QSApi._raise_request_error(resp)

        return json_resp

    @staticmethod
    def _get_failure_message(resp) -> str:
        request_url = resp.request.url
        return f'Failed to call {request_url}.  Status code: "{resp.status_code}", body: "{resp.text}"'

    @staticmethod
    def _raise_request_failure(url, ex:RequestException):
        raise QSException(f'Request to {url} failed: {str(ex)}') from ex

    @staticmethod
    def _raise_request_error(resp):
        raise QSException(QSApi._get_failure_message(resp))

    @staticmethod
    def _build_control_url(base_uri:str, key:str, device:str, level:int) -> str:
        return urljoin(base_uri,
                       f'control/{quote_plus(key)}/' +
                       f'?device={quote_plus(device)}&setlevel={level}')