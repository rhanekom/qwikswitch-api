from requests import RequestException
from urllib.parse import urljoin, quote_plus

from qwikswitchapi.constants import DEFAULT_BASE_URI
from qwikswitchapi.exceptions import QSAuthException, QSRequestFailedException, QSRequestErrorException


class ResponseParser:

    @staticmethod
    def get_failure_message(resp) -> str:
        """
        Returns a formatted message indicating the request failed
        :param resp: The response object
        :return: A formatted message indicating the request failed
        """
        request_url = resp.request.url
        return f'Failed to call {request_url}.  Status code: "{resp.status_code}", body: "{resp.text}"'

    @staticmethod
    def raise_request_failure(url, ex: RequestException):
        """
        Raises a QSException indicating the request failed
        :param url: The URL of the request
        :param ex: The exception that was raised
        :raises QSException: Indicating the request failed, chained with the original exception.
        """
        raise QSRequestFailedException(f'Request to {url} failed: {str(ex)}') from ex

    @staticmethod
    def raise_request_error(resp):
        """
        Raises a QSException indicating the request failed
        :param resp: The response object
        :raises QSException: Indicating the request failed, with the body of the response.
        """
        raise QSRequestErrorException(ResponseParser.get_failure_message(resp))

    @staticmethod
    def raise_auth_failure(resp):
        """
        Raises a QSAuthException indicating the request failed
        :param resp: The response object
        :raises QSException: Indicating the request failed, with the body of the response.
        """
        raise QSAuthException(ResponseParser.get_failure_message(resp))




class UrlBuilder:

    @staticmethod
    def build_get_all_device_status_url(key: str, base_uri: str = DEFAULT_BASE_URI) -> str:
        """
        Builds the URL to get the status of all devices
        :param base_uri: The base URI to use
        :param key: The API key to use
        :return: The url to the 'Get all device status' endpoint
        """
        return urljoin(base_uri, f'state/{quote_plus(key)}/')

    @staticmethod
    def build_generate_api_keys_url(base_uri:str = DEFAULT_BASE_URI) -> str:
        """
        Builds the URL to generate API keys
        :param base_uri: The base URI to use
        :return: The url to the 'Generate API keys' endpoint
        """
        return urljoin(base_uri, 'keys')

    @staticmethod
    def build_delete_api_keys_url(base_uri: str = DEFAULT_BASE_URI) -> str:
        """
        Builds the URL to delete API keys
        :param base_uri: The base URI to use
        :return: The url to the 'Delete API keys' endpoint
        """
        return urljoin(base_uri, 'keys/delete/')

    @staticmethod
    def build_control_url(key: str, device_id: str, level: int, base_uri: str = DEFAULT_BASE_URI) -> str:
        """
        Builds the URL to control a device
        :param base_uri: The base URI to use
        :param key: The API key to use
        :param device_id: The unique identifier of the device to control
        :param level: The level to set the device to
        :return: The url to the `Control a device` endpoint
        """
        return urljoin(base_uri,
                       f'control/{quote_plus(key)}/' +
                       f'?device={quote_plus(device_id)}&setlevel={level}')