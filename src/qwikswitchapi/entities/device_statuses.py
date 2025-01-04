from __future__ import annotations

from typing import List

from src.qwikswitchapi.entities.device_status import DeviceStatus
from src.qwikswitchapi.utility.response_parser import ResponseParser


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

        if ('success' in json_data and json_data['success'] == False) or ('error' in json_data):
            ResponseParser.raise_request_error(resp)

        statuses = []

        for key in json_data:
            if key != 'success':
                statuses.append(DeviceStatus.from_json({key : json_data[key]}))

        return cls(statuses)
