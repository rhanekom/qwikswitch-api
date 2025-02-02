"""Utility methods for handling urls and parsing response messages."""

from typing import Never
from urllib.parse import quote_plus, urljoin

from requests import RequestException

from .constants import DEFAULT_BASE_URI
from .exceptions import (
    QSAuthError,
    QSRequestError,
    QSRequestFailedError,
)


class ResponseParser:
    """Utility methods to parse and validate HTTP responses."""

    @staticmethod
    def get_failure_message(resp) -> str:  # noqa: ANN001
        """
        Return a formatted message indicating the request failed.

        :param resp: The response object
        :return: A formatted message indicating the request failed
        """
        request_url = resp.request.url
        return (
            f'Failed to call {request_url}.  Status code: "{resp.status_code}", '
            f'body: "{resp.text}"'
        )

    @staticmethod
    def raise_request_failure(url, ex: RequestException) -> Never:  # noqa: ANN001
        """
        Raise a QSRequestFailedError indicating the request failed.

        :param url: The URL of the request
        :param ex: The exception that was raised
        :raises QSRequestFailedError: Indicating the request failed, chained with the original exception.
        """
        msg = f"Request to {url} failed: {ex!s}"
        raise QSRequestFailedError(msg) from ex

    @staticmethod
    def raise_request_error(resp) -> Never:  # noqa: ANN001
        """
        Raise a QSRequestError indicating the request failed.

        :param resp: The response object
        :raises QSRequestError: Indicating the request failed, with the body of the response.
        """
        raise QSRequestError(ResponseParser.get_failure_message(resp))

    @staticmethod
    def raise_auth_failure(resp) -> Never:  # noqa: ANN001
        """
        Raise a QSAuthException indicating the request failed.

        :param resp: The response object
        :raises QSAuthError: Indicating the request failed, with the body of the response.
        """
        raise QSAuthError(ResponseParser.get_failure_message(resp))


class UrlBuilder:
    """Utility methods to build URLs for the Qwikswitch API."""

    @staticmethod
    def build_get_all_device_status_url(
        key: str, base_uri: str = DEFAULT_BASE_URI
    ) -> str:
        """
        Build the URL to get the status of all devices.

        :param base_uri: The base URI to use
        :param key: The API key to use
        :return: The url to the 'Get all device status' endpoint
        """
        return urljoin(base_uri, f"state/{quote_plus(key)}/")

    @staticmethod
    def build_generate_api_keys_url(base_uri: str = DEFAULT_BASE_URI) -> str:
        """
        Build the URL to generate API keys.

        :param base_uri: The base URI to use
        :return: The url to the 'Generate API keys' endpoint
        """
        return urljoin(base_uri, "keys")

    @staticmethod
    def build_delete_api_keys_url(base_uri: str = DEFAULT_BASE_URI) -> str:
        """
        Build the URL to delete API keys.

        :param base_uri: The base URI to use
        :return: The url to the 'Delete API keys' endpoint
        """
        return urljoin(base_uri, "keys/delete/")

    @staticmethod
    def build_control_url(
        key: str, device_id: str, level: int, base_uri: str = DEFAULT_BASE_URI
    ) -> str:
        """
        Build the URL to control a device.

        :param base_uri: The base URI to use
        :param key: The API key to use
        :param device_id: The unique identifier of the device to control
        :param level: The level to set the device to
        :return: The url to the `Control a device` endpoint
        """
        return urljoin(
            base_uri,
            f"control/{quote_plus(key)}/"
            f"?device={quote_plus(device_id)}&setlevel={level}",
        )
