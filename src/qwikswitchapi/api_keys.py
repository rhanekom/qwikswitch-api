from __future__ import annotations

class ApiKeys:
    def __init__(self, read_key:str, read_write_key:str):
        self._read_key = read_key
        self._read_write_key = read_write_key

    @property
    def read_key(self) -> str:
        return self._read_key

    @property
    def read_write_key(self) -> str:
        return self._read_write_key

    @classmethod
    def from_json(cls, json_data) -> ApiKeys:
        return cls(json_data['r'], json_data['rw'])