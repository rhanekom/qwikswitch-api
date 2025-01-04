# qwikswitch-api

A Python wrapper for the [Qwikswitch API](https://qwikswitch.com/doc/), used for remotely controlling [Qwikswitch](https://qwikswitch.com/) devices using the [Wifi Bridge](https://www.qwikswitch.co.za/products/wifi-bridge).

An alternative (local) way of controlling Qwikswitch devices is with a USB Modem.  If this is the device that you have, see the [pyqwikswitch library](https://github.com/kellerza/pyqwikswitch) instead.

## Usage

The following operations are implemented:
* Keys - Generate API Keys (`generate_api_keys`)
* Keys - Delete API Keys (`delete_api_keys`)
* Control - Control a device (`control_device`)
* State - Get all device status (`get_all_device_status`)

Device history is *not* implemented in this library yet as I don't have access to these devices.  

If you have access to devices that record history, please open an issue detailing sample responses from `get_all_device_status` and the history calls. 

Sample usage to control a device:

```python
from qwikswitch import QSApi

api = Qwikswitch('email', 'masterkey')
api_keys = api.generate_api_keys()
api.control_device(api_keys, '@123450', 100)
```

To list all current device statuses:

```python
```python
devices = api.get_all_device_status(api_keys)
```

