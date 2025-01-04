from __future__ import annotations

class DeviceStatus:
    def __init__(self, device_type:str, firmware:str, epoch:int, rssi:int, value:int):
        """
        Initializes a DeviceStatus object
        :param device_type: the type of device
        :param firmware: the version of the device firmware
        :param epoch: the epoch time of the last status update
        :param rssi: the signal strength of the device
        :param value: the current value of the device
        """
        self._device_type = device_type
        self._firmware = firmware
        self._epoch = epoch
        self._rssi = rssi
        self._value = value

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
        :return: A ControlResult object
        """
        rssi = int(json_data['rssi'].replace('%', ''))
        return cls(
            json_data['type'],
            json_data['firmware'],
            json_data['epoch'],
            rssi,
            json_data['value']
        )