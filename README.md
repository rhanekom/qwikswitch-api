# qwikswitch-api

[![PyPI version](https://img.shields.io/pypi/v/qwikswitch-api.svg)](https://pypi.org/project/qwikswitch-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/qwikswitch-api.svg)](https://pypi.org/project/qwikswitch-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python wrapper for the [QwikSwitch API](https://qwikswitch.com/doc/), used to remotely
control [QwikSwitch](https://qwikswitch.com/) home-automation devices (relays and dimmers)
through the [Wi-Fi Bridge](https://www.qwikswitch.co.za/products/wifi-bridge).

> **Using a USB modem instead?**
> This library talks to the *cloud* API exposed by the Wi-Fi Bridge. If you control your
> devices locally over a USB modem, use the [pyqwikswitch](https://github.com/kellerza/pyqwikswitch)
> library instead.

## Installation

```bash
pip install qwikswitch-api
```

Or, with [uv](https://docs.astral.sh/uv/):

```bash
uv add qwikswitch-api
```

Requires **Python 3.14+**. The only runtime dependency is [`requests`](https://pypi.org/project/requests/).

> **Note:** the distribution is published as `qwikswitch-api`, but the import package is
> `qwikswitchapi` (no hyphen):
>
> ```python
> from qwikswitchapi.client import QSClient
> ```

## Quick start

```python
from qwikswitchapi.client import QSClient

# `master_key` is the 12-character key found under your CloudHub — it is the
# device id of your QwikSwitch Wi-Fi Bridge.
client = QSClient("you@example.com", "your-master-key")

# Turn a device fully on (level 100), or off (level 0). For dimmers, any value
# between 1 and 100 sets the brightness.
result = client.control_device("@123450", 100)
print(result.device_id, "->", result.level)

# Read the status of every device registered to your bridge.
statuses = client.get_all_device_status()
for device in statuses.statuses:
    print(device.device_id, device.device_type, device.device_class, device.value)
```

## Authentication

The QwikSwitch API is called with short-lived API keys that are derived from your
email address and master key. You do **not** need to manage these manually:

- The client authenticates **lazily** — the first call to `control_device` or
  `get_all_device_status` automatically calls `generate_api_keys` for you.
- You can also generate them explicitly, inspect them, or reuse them:

```python
client = QSClient("you@example.com", "your-master-key")

keys = client.generate_api_keys()   # returns an ApiKeys object
print(keys.read_key)                 # read-only key
print(keys.read_write_key)           # read/write key (also grants read access)

# The most recently generated keys are available on the client:
client.api_keys

# Revoke the keys generated for this email / master key:
client.delete_api_keys()
```

## API reference

### `QSClient(email, master_key, base_uri="https://qwikswitch.com/api/v1/")`

The central class wrapping all API operations.

| Method | Returns | Description |
| --- | --- | --- |
| `generate_api_keys()` | `ApiKeys` | Generate read and read/write API keys. Called automatically on the first authenticated request. |
| `delete_api_keys()` | `None` | Delete the API keys generated for this email / master key. |
| `control_device(device_id, level)` | `ControlResult` | Set a device to `level` (`0` = off, `1`–`100` = on / brightness). |
| `get_all_device_status()` | `DeviceStatuses` | Retrieve the status of all devices registered to the keys. |

### Return objects

**`ApiKeys`** — `read_key`, `read_write_key`.

**`ControlResult`** — `device_id`, `level` (the level the device was set to).

**`DeviceStatuses`** — `statuses`, a list of `DeviceStatus`.

**`DeviceStatus`**

| Property | Type | Description |
| --- | --- | --- |
| `device_id` | `str` | Unique device identifier. |
| `device_type` | `str` | Device model string (e.g. `"RELAY QS-D-S5"`). |
| `firmware` | `str` | Device firmware version. |
| `epoch` | `int` | Epoch time of the last status update. |
| `rssi` | `int` | Signal strength as a percentage (0–100). |
| `value` | `int` | Current value (`0` = off, `1`–`100` = on). |
| `device_class` | `DeviceClass` | Classified device type (see below), or `DeviceClass.unknown`. |

**`DeviceClass`** (enum): `relay`, `dimmer`, `humidity_temperature`, `unknown`.

## Supported devices

| Model | Type | `DeviceClass` |
| --- | --- | --- |
| `RELAY QS-D-S5` | Dimmer | `dimmer` |
| `RELAY QS-R-S5` | Relay | `relay` |
| `RELAY QS-R-S30` | Relay | `relay` |

Any other model is reported with `device_class == DeviceClass.unknown`. If you have a
device that isn't listed, please [open an issue](https://github.com/rhanekom/qwikswitch-api/issues)
with the model name and device type so it can be added.

## Error handling

All errors raised by the library derive from a single base exception, `QSError`, so you
can catch everything with one `except`:

```python
from qwikswitchapi.exceptions import QSError

try:
    client.control_device("@123450", 100)
except QSError as exc:
    print("QwikSwitch call failed:", exc)
```

The hierarchy is:

```text
QSError
├── QSAuthError            # authentication / key generation failed
├── QSRequestFailedError   # the HTTP request itself failed (network, etc.)
└── QSRequestError         # the API returned an error response
    └── QSResponseParseError  # the response could not be validated / parsed
```

## Limitations

- **Device history is not implemented yet** — the author does not have access to devices
  that record history. If you do, please [open an issue](https://github.com/rhanekom/qwikswitch-api/issues)
  with sample responses from `get_all_device_status` and the history calls, and it can be added.

## Contributing

Issues and pull requests are welcome.

## License

Distributed under the [MIT License](https://opensource.org/licenses/MIT).
