from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException

from src.qwikswitchapi.entities.api_keys import ApiKeys
from src.qwikswitchapi.entities.control_result import ControlResult
from src.qwikswitchapi.utility.response_parser import ResponseParser
from src.qwikswitchapi.utility.url_builder import UrlBuilder


class QSApi:
    DEFAULT_BASE_URI = 'https://qwikswitch.com/api/v1/'

    def __init__(self, email:str, master_key:str, base_uri:str=DEFAULT_BASE_URI):
        """
        Initializes a new instance of the QSApi class

        :param email: your email address registered on https://qwikswitch.com
        :param master_key: 12 character key found under your CloudHub.  This should be your device id of your Qwikswitch Wi-Fi bridge.
        :param base_uri: the base URI of the Qwikswitch API, optional.  Defaults to 'https://qwikswitch.com/api/v1/'
        """

        self._email = email
        self._master_key = master_key

        if not base_uri.endswith('/'):
            base_uri += '/'

        self._base_uri = base_uri

    @property
    def base_uri(self) -> str:
        """
        The base URI of the Qwikswitch API

        :returns: The base URI of the Qwikswitch API
        """

        return self._base_uri

    def generate_api_keys(self) -> ApiKeys:
        """
        Generates API keys for the given email and master key to be used in subsequent calls

        :returns: APIKeys, with an API key for read operations, and one for read-write operations.
        :raises QSException: on failure to generate API keys
        """

        url = UrlBuilder.build_generate_api_keys_url(self._base_uri)
        req = {
            'email': self._email,
            'master_key': self._master_key
        }

        try:
            resp = requests.post(url, json=req)
            json_resp = QSApi._parse_response(resp)
            return ApiKeys.from_json(json_resp)
        except RequestException as ex:
            ResponseParser.raise_request_failure(url, ex)

    def control_device(self, auth:ApiKeys, device_id:str, level:int):
        """
        Controls a device by setting the desired level.

        :param auth: authentication keys generated by generate_api_keys
        :param device_id: the unique identifier of the device to control
        :param level: this is a description of what is returned
        :returns: ControlResult, with the device and level set
        :raises QSException: when the request fails
        """

        url = UrlBuilder.build_control_url(self._base_uri, auth.read_write_key, device_id, level)

        try:
            resp = requests.get(url)
            json_resp = QSApi._parse_response(resp)
            return ControlResult.from_json(json_resp)
        except RequestException as ex:
            ResponseParser.raise_request_failure(url, ex)

    def get_all_device_status(self, auth:ApiKeys):
        """
        Retrieves the status of all devices registered to the given API keys

        :param auth: authentication keys generated by generate_api_keys
        :returns: Array of DeviceStatus with device information
        :raises QSException: when the request fails
        """

        url = UrlBuilder.build_get_all_device_status_url(self._base_uri, auth.read_write_key)

        try:
            resp = requests.get(url)
            json_resp = QSApi._parse_response(resp)
            return ControlResult.from_json(json_resp)
        except RequestException as ex:
            ResponseParser.raise_request_failure(url, ex)

    @staticmethod
    def _parse_response(resp) -> dict:
        if resp.status_code != 200:
            ResponseParser.raise_request_error(resp)

        json_resp = resp.json()

        if 'err' in json_resp:
            ResponseParser.raise_request_error(resp)
        if 'ok' in json_resp and json_resp['ok'] == 0:
            ResponseParser.raise_request_error(resp)
        if 'success' in json_resp and json_resp['success'] == False:
            ResponseParser.raise_request_error(resp)
        if 'error' in json_resp and "No Data" not in json_resp['error']:
            ResponseParser.raise_request_error(resp)

        return json_resp


