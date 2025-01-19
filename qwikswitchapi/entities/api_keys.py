from __future__ import annotations

from qwikswitchapi.constants import JsonKeys
from qwikswitchapi.utility.response_parser import ResponseParser

class ApiKeys:
    def __init__(self, read_key:str, read_write_key:str):
        """
        Initializes an ApiKeys object

        :param read_key: The API key used for read operations.
        :param read_write_key: The API key used for read-write operations.
        """
        self._read_key = read_key
        self._read_write_key = read_write_key

    @property
    def read_key(self) -> str:
        """
        The API key for read operations (no device control)
        :return: the read API key
        """
        return self._read_key

    @property
    def read_write_key(self) -> str:
        """
        The API key for read-write operations (device control).  Can also be used for read access.
        :return: the read/write API key
        """
        return self._read_write_key

    @classmethod
    def from_resp(cls, resp) -> ApiKeys:
        """
        Constructs an ApiKeys object from JSON data
        :param resp: The response object to construct the object from
        :return: the ApiKeys object
        :raises QSException: on failure of the response, or validation error
        """
        if resp.status_code != 200:
            ResponseParser.raise_auth_failure(resp)

        json_data = resp.json()

        if ((JsonKeys.OK in json_data and json_data[JsonKeys.OK] == 0) or
                (JsonKeys.ERR in json_data)):
            ResponseParser.raise_auth_failure(resp)

        return cls(json_data[JsonKeys.READ_KEY], json_data[JsonKeys.READ_WRITE_KEY])