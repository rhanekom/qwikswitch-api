from urllib.parse import urljoin, quote_plus

from src.qwikswitchapi.constants import Constants

class UrlBuilder:

    @staticmethod
    def build_get_all_device_status_url(key: str, base_uri: str = Constants.DEFAULT_BASE_URI) -> str:
        """
        Builds the URL to get the status of all devices
        :param base_uri: The base URI to use
        :param key: The API key to use
        :return: The url to the 'Get all device status' endpoint
        """
        return urljoin(base_uri, f'state/{quote_plus(key)}/')

    @staticmethod
    def build_generate_api_keys_url(base_uri:str = Constants.DEFAULT_BASE_URI) -> str:
        """
        Builds the URL to generate API keys
        :param base_uri: The base URI to use
        :return: The url to the 'Generate API keys' endpoint
        """
        return urljoin(base_uri, 'keys')

    @staticmethod
    def build_control_url(key: str, device_id: str, level: int, base_uri: str = Constants.DEFAULT_BASE_URI) -> str:
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