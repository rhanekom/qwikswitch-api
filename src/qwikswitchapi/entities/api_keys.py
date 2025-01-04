from __future__ import annotations

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
    def from_json(cls, json_data) -> ApiKeys:
        """
        Constructs an ApiKeys object from JSON data
        :return: the ApiKeys object
        """
        return cls(json_data['r'], json_data['rw'])