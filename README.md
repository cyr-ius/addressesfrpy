# AddressesFrPy

Asynchronous Python client for querying the French geocoding API [Géoplateforme IGN](https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage).

[![PyPI version](https://badge.fury.io/py/addressesfrpy.svg)](https://badge.fury.io/py/addressesfrpy)
[![Python](https://img.shields.io/pypi/pyversions/addressesfrpy)](https://pypi.org/project/addressesfrpy/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Features

- **Address search**: free-text search with filters (postcode, city, type, category...)
- **Reverse geocoding**: find an address from GPS coordinates
- **Supported indexes**: `address`, `poi` (points of interest), `parcel`
- **Fully asynchronous** via `asyncio` and `aiohttp`

## Installation

```bash
pip install addressesfrpy
```

## Requirements

- Python >= 3.10
- `aiohttp >= 3.8.1`

## Usage

### Address search

```python
import asyncio
from addressesfrpy import AddressFr
from addressesfrpy.exceptions import AddressFrException

async def main():
    api = AddressFr()

    addresses = await api.async_search("8 boulevard du Port, Cergy", limit=5)
    for address in addresses:
        print(address["properties"]["label"])
        print(address["geometry"]["coordinates"])

    await api.async_close()

asyncio.run(main())
```

### Reverse geocoding

```python
async def main():
    api = AddressFr()

    addresses = await api.async_reverse(lon=2.3488, lat=48.8534, index="address")
    for address in addresses:
        print(address["properties"]["label"])

    await api.async_close()
```

### Using an existing aiohttp session

```python
from aiohttp import ClientSession
from addressesfrpy import AddressFr

async def main():
    async with ClientSession() as session:
        api = AddressFr(session=session)
        addresses = await api.async_search("Paris", limit=3, index="poi")
```

## API Reference

### `AddressFr(session=None, timeout=120)`

| Parameter | Type                    | Description                               |
| --------- | ----------------------- | ----------------------------------------- |
| `session` | `ClientSession \| None` | Existing aiohttp session (optional)       |
| `timeout` | `int`                   | Request timeout in seconds (default: 120) |

### `async_search(query, limit=10, **kwargs)`

Search for addresses by free text.

| Parameter            | Type    | Description                                      |
| -------------------- | ------- | ------------------------------------------------ |
| `query`              | `str`   | Search text                                      |
| `limit`              | `int`   | Maximum number of results (default: 10)          |
| `index`              | `str`   | Target index: `address`, `poi`, `parcel`         |
| `autocomplete`       | `bool`  | Enable autocomplete suggestions                  |
| `lat` / `lon`        | `float` | Coordinates to prioritise the search             |
| `postcode`           | `str`   | Filter by postcode                               |
| `citycode`           | `str`   | Filter by INSEE city code                        |
| `type`               | `str`   | Address type: `street`, `city`, etc.             |
| `city`               | `str`   | Filter by city name                              |
| `category`           | `str`   | Filter by category (e.g. `restaurant`, `school`) |
| `departmentcode`     | `str`   | Filter by department code                        |
| `returntruegeometry` | `bool`  | Return the true geometry                         |

### `async_reverse(**kwargs)`

Reverse geocoding from GPS coordinates.

| Parameter    | Type    | Description                              |
| ------------ | ------- | ---------------------------------------- |
| `lon`        | `float` | Longitude                                |
| `lat`        | `float` | Latitude                                 |
| `index`      | `str`   | Target index: `address`, `poi`, `parcel` |
| `limit`      | `int`   | Maximum number of results                |
| `searchgeom` | `str`   | Search geometry type (e.g. `polygon`)    |

### `async_close()`

Close the HTTP session.

## Exceptions

| Exception              | Description                            |
| ---------------------- | -------------------------------------- |
| `AddressFrException`   | Base exception for the client          |
| `AddressNotFound`      | No address found for the query         |
| `HttpRequestError`     | Error while communicating with the API |
| `TimeoutExceededError` | Request timed out                      |
| `RequestException`     | HTTP error returned by the server      |

## Response format

Methods return a list of features in **GeoJSON** format:

```json
[
  {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [2.3488, 48.8534]
    },
    "properties": {
      "label": "75001 Paris",
      "name": "Paris",
      "_type": "municipality",
      "postcode": "75001",
      "citycode": "75056"
    }
  }
]
```

## License

GPL-3.0-or-later — see the [LICENSE](LICENSE) file.
