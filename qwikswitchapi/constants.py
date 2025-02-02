"""Constants for the Qwikswitch API."""

from enum import Enum
from typing import Final

DEFAULT_BASE_URI: Final = "https://qwikswitch.com/api/v1/"
DEFAULT_TIMEOUT: Final = 10000


class JsonKeys:
    """Constants for names of Json keys."""

    OK: Final = "ok"
    SUCCESS: Final = "success"
    ERROR: Final = "error"
    ERR: Final = "err"
    READ_KEY: Final = "r"
    READ_WRITE_KEY: Final = "rw"
    DEVICE: Final = "device"
    LEVEL: Final = "level"
    RSSI: Final = "rssi"
    TYPE: Final = "type"
    FIRMWARE: Final = "firmware"
    EPOCH: Final = "epoch"
    VALUE: Final = "value"
    EMAIL: Final = "email"
    MASTER_KEY: Final = "masterKey"


class DeviceClass(Enum):
    """Enum for device classes."""

    relay = 1
    dimmer = 2
    humidity_temperature = 3
    unknown = 999


DEVICES = {
    "RELAY QS-D-S5": DeviceClass.dimmer,
    "RELAY QS-R-S5": DeviceClass.relay,
    "RELAY QS-R-S30": DeviceClass.relay,
    # Add more devices here
}
