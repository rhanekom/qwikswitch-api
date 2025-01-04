from __future__ import annotations

from typing import List

from src.qwikswitchapi.entities.device_status import DeviceStatus

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