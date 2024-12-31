from urllib.parse import urljoin

import requests

from src.qwikswitchapi.apikeys import ApiKeys
from src.qwikswitchapi.qsexception import QSException

DEFAULT_BASE_URI='https://qwikswitch.com/api/v1/'

class QSApi:
    def __init__(self, email, master_key, base_uri=DEFAULT_BASE_URI):
        self._email = email
        self._master_key = master_key
        self._base_uri = base_uri

    def generate_api_keys(self):
        url = urljoin(self._base_uri, 'keys')
        req = {
            'email': self._email,
            'master_key': self._master_key
        }
        resp = requests.post(url, json=req)

        if resp.status_code == 200:
            json_resp = resp.json()

            if 'err' in json_resp:
                raise QSException(f'Failed to generate API keys: {json_resp["err"]}')
            if 'ok' in json_resp and json_resp['ok'] == 0:
                raise QSException(f'Failed to generate API keys: {json_resp}')

            return ApiKeys.from_json(json_resp)
        else:
            raise QSException(f'Failed to generate API keys with status code {resp.status_code}, body: {resp.text}')