from enum import Enum


class Constants:
    DEFAULT_BASE_URI = 'https://qwikswitch.com/api/v1/'

    class JsonKeys:
        OK = 'ok'
        SUCCESS = 'success'
        ERROR = 'error'
        ERR = 'err'
        READ_KEY = 'r'
        READ_WRITE_KEY = 'rw'
        DEVICE = 'device'
        LEVEL = 'level'
        RSSI = 'rssi'
        TYPE = 'type'
        FIRMWARE = 'firmware'
        EPOCH = 'epoch'
        VALUE = 'value'

    class DeviceClass(Enum):
        relay = 1
        dimmer = 2
        humidity_temperature = 3 
        unknown = 999

    DEVICES = {
        "RELAY QS-D-S5" : DeviceClass.dimmer,
        "RELAY QS-R-S5" : DeviceClass.relay,
        "RELAY QS-R-S30" : DeviceClass.relay
        # Add more devices here
    }

