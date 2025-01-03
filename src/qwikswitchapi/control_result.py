from __future__ import annotations

class ControlResult:
    def __init__(self, device:str, level:int):
        self._device = device
        self._level = level

    @property
    def device(self):
        return self._device

    @property
    def level(self):
        return self._level

    @classmethod
    def from_json(cls, json_data) -> ControlResult:
        return cls(json_data['device'], json_data['level'])