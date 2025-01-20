from __future__ import annotations

from typing import List, Any

from qwikswitchapi.utility import ResponseParser
from qwikswitchapi.constants import DeviceClass, DEVICES, JsonKeys
from qwikswitchapi.exceptions import QSException


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

        if ((JsonKeys.SUCCESS in json_data and json_data[JsonKeys.SUCCESS] == False)
                or (JsonKeys.ERROR in json_data)):
            ResponseParser.raise_request_error(resp)

        return cls(json_data[JsonKeys.DEVICE], json_data[JsonKeys.LEVEL])


class DeviceStatus:
    def __init__(self,
                 device_id:str,
                 device_type:str,
                 firmware:str,
                 epoch:int,
                 rssi:int,
                 value:int):
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

    @property
    def device_class (self) -> DeviceClass | Any:
        """
        The class of the device
        :return: The class of the device
        """
        if self._device_type in DEVICES:
            return DEVICES[self._device_type]
        else:
            return DeviceClass.unknown

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

        rssi = int(state_json_data[JsonKeys.RSSI].replace('%', ''))
        return cls(
            device_id,
            state_json_data[JsonKeys.TYPE],
            state_json_data[JsonKeys.FIRMWARE],
            state_json_data[JsonKeys.EPOCH],
            rssi,
            state_json_data[JsonKeys.VALUE]
        )


class DeviceStatuses:
    def __init__(self, statuses:List[DeviceStatus]):
        """
        Initializes a DeviceStatuses object
        :param statuses: The list of device statuses
        """
        self._statuses = statuses

    @property
    def statuses(self):
        """
        The list of device statuses
        :return: The list of device statuses
        """
        return self._statuses

    @classmethod
    def from_resp(cls, resp) -> DeviceStatuses:
        if resp.status_code != 200:
            ResponseParser.raise_request_error(resp)

        json_data = resp.json()

        if ((JsonKeys.SUCCESS in json_data and json_data[JsonKeys.SUCCESS] == False)
                or (JsonKeys.ERROR in json_data)):
            ResponseParser.raise_request_error(resp)

        statuses = []

        for key in json_data:
            if key != JsonKeys.SUCCESS:
                statuses.append(DeviceStatus.from_json({key : json_data[key]}))

        return cls(statuses)
