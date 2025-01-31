import requests
from requests.exceptions import RequestException
import functools

from qwikswitchapi.constants import JsonKeys, DEFAULT_BASE_URI
from qwikswitchapi.entities import ApiKeys, ControlResult, DeviceStatuses
from qwikswitchapi.utility import ResponseParser
from qwikswitchapi.utility import UrlBuilder

class QSClient:

    def _ensure_authenticated(func):
        @functools.wraps(func)
        def authenticate_if_needed(self, *args, **kwargs):
            if self._api_keys is None:
                self.generate_api_keys()
            return func(self, *args, **kwargs)

        return authenticate_if_needed

    def _handle_request_failure(func):
        @functools.wraps(func)
        def catch_failure(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RequestException as ex:
                url = ex.request.url if ex.request is not None else "Unknown"
                ResponseParser.raise_request_failure(url, ex)

        return catch_failure

    def __init__(self, email:str, master_key:str, base_uri:str=DEFAULT_BASE_URI):
        """
        Initializes a new instance of the QSApi class

        :param email: the email address to generate API keys for:param email: your email address registered on https://qwikswitch.com
        :param master_key: 12 character key found under your CloudHub.  This should be your device id of your Qwikswitch Wi-Fi bridge.
        :param base_uri: the base URI of the Qwikswitch API, optional.  Defaults to 'https://qwikswitch.com/api/v1/'
        """

        self._email = email
        self._master_key = master_key
        self._api_keys = None

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

    @_handle_request_failure
    def generate_api_keys(self) -> ApiKeys:
        """
        Generates API keys for the given email and master key to be used in subsequent calls

        :returns: APIKeys, with an API key for read operations, and one for read-write operations.
        :raises QSException: on failure to generate API keys
        """

        url = UrlBuilder.build_generate_api_keys_url(self._base_uri)
        req = {
            JsonKeys.EMAIL: self._email,
            JsonKeys.MASTER_KEY: self._master_key
        }

        resp = requests.post(url, json=req)
        self._api_keys = ApiKeys.from_resp(resp)
        return self._api_keys

    @_handle_request_failure
    def delete_api_keys(self) -> None:
        """
        Deletes API keys generated for the given email and master key

        :returns: None
        :raises QSException: on failure to delete API keys
        """

        url = UrlBuilder.build_delete_api_keys_url(self._base_uri)
        req = {
            JsonKeys.EMAIL: self._email,
            JsonKeys.MASTER_KEY: self._master_key
        }

        resp = requests.post(url, json=req)
        _ = ApiKeys.from_resp(resp)

    @_ensure_authenticated
    @_handle_request_failure
    def control_device(self, device_id:str, level:int) -> ControlResult:
        """
        Controls a device by setting the desired level.

        :param device_id: the unique identifier of the device to control
        :param level: this is a description of what is returned
        :returns: ControlResult, with the device and level set
        :raises QSException: when the request fails
        """

        url = UrlBuilder.build_control_url(self._api_keys.read_write_key, device_id, level, self._base_uri)

        resp = requests.get(url)
        return ControlResult.from_resp(resp)

    @_ensure_authenticated
    @_handle_request_failure
    def get_all_device_status(self) -> DeviceStatuses:
        """
        Retrieves the status of all devices registered to the given API keys

        :param auth: authentication keys generated by generate_api_keys
        :returns: Array of DeviceStatus with device information
        :raises QSException: when the request fails
        """

        url = UrlBuilder.build_get_all_device_status_url(self._api_keys.read_write_key, self._base_uri)

        resp = requests.get(url)
        return DeviceStatuses.from_resp(resp)

    _ensure_authenticated = staticmethod(_ensure_authenticated)
    _handle_request_failure = staticmethod(_handle_request_failure)

