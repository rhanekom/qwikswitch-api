from __future__ import annotations

from src.qwikswitchapi.qs_exception import QSException
from src.qwikswitchapi.utility.response_parser import ResponseParser


class DeviceStatus:
    def __init__(self, device_id:str, device_type:str, firmware:str, epoch:int, rssi:int, value:int):
        """
        Initializes a DeviceStatus object
        :param device_id: the unique device identifier
        :param device_type: the type of device
        :param firmware: the version of the device firmware
        :param epoch: the epoch time of the last status update
        :param rssi: the signal strength of the device
        :param value: the current value of the device
        """
        self._device_id = device_id
        self._device_type = device_type
        self._firmware = firmware
        self._epoch = epoch
        self._rssi = rssi
        self._value = value

    @property
    def device_id(self) -> str:
        """
        The unique identifier of the device
        :return: the unique identifier of the device
        """
        return self._device_id

    @property
    def device_type(self) -> str:
        """
        The type of device
        :return: the type of device
        """
        return self._device_type

    @property
    def firmware(self) -> str:
        """
        The version of the device firmware
        :return: The version of the device firmware
        """
        return self._firmware

    @property
    def epoch(self) -> int:
        """
        The epoch time of the last status update
        :return: The epoch time of the last status update
        """
        return self._epoch

    @property
    def rssi(self) -> int:
        """
        The signal strength of the device
        :return: The signal strength of the device (percentage, 0 - 100)
        """
        return self._rssi

    @property
    def value(self) -> int:
        """
        The current value of the device
        :return: The current value of the device. [0=off 1-100=on]
        """
        return self._value

    @classmethod
    def from_json(cls, json_data) -> DeviceStatus:
        """
        Constructs a DeviceStatus object from JSON data
        :param json_data: The JSON data to construct the object from
        :return: A DeviceStatus object
        :raises QSException: on validation error
        """

        if len(json_data) > 1:
            raise QSException('Invalid JSON data for DeviceStatus')

        device_id = next(iter(json_data)) # Only expecting one key
        state_json_data = json_data[device_id]

        rssi = int(state_json_data['rssi'].replace('%', ''))
        return cls(
            device_id,
            state_json_data['type'],
            state_json_data['firmware'],
            state_json_data['epoch'],
            rssi,
            state_json_data['value']
        )