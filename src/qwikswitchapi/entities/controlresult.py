from __future__ import annotations

from src.qwikswitchapi.constants import Constants
from src.qwikswitchapi.utility.responseparser import ResponseParser


class ControlResult:
    def __init__(self, device_id:str, level:int):
        """
        Initializes a ControlResult object
        :param device_id: the unique device identifier
        :param level: The final level to which the device was set
        """
        self._device_id = device_id
        self._level = level

    @property
    def device_id(self):
        """
        The unique identifier of the device
        :return: The unique identifier of the device
        """
        return self._device_id

    @property
    def level(self):
        """
        The level to which the device was set
        :return: The level to which the device was set
        """
        return self._level

    @classmethod
    def from_resp(cls, resp) -> ControlResult:
        """
        Constructs a ControlResult object from JSON data
        :param resp: The response object to construct the object from
        :return: A ControlResult object
        :raises QSException: on failure of the response, or validation error
        """
        if resp.status_code != 200:
            ResponseParser.raise_request_error(resp)

        json_data = resp.json()

        if ((Constants.JsonKeys.SUCCESS in json_data and json_data[Constants.JsonKeys.SUCCESS] == False)
                or (Constants.JsonKeys.ERROR in json_data)):
            ResponseParser.raise_request_error(resp)

        return cls(json_data[Constants.JsonKeys.DEVICE], json_data[Constants.JsonKeys.LEVEL])