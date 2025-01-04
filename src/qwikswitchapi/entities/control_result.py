from __future__ import annotations

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
    def from_json(cls, json_data) -> ControlResult:
        """
        Constructs a ControlResult object from JSON data
        :param json_data: The JSON data to construct the object from
        :return: A ControlResult object
        """
        return cls(json_data['device'], json_data['level'])