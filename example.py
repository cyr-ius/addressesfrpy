"""Example script to demonstrate the usage of the AddressFr class for asynchronous address searching and reverse geocoding."""

import asyncio
import logging

from addressesfrpy import AddressFr, AddressFrException

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


async def async_main() -> None:
    """Instantiate class."""
    api = AddressFr()

    # Example of searching for addresses
    try:
        addresses = await api.async_search("Paris", limit=5, index="poi")
        for address in addresses:
            logger.info("Address: %s", address)
    except AddressFrException as err:
        logger.error(err)
        return

    # Example of reverse geocoding
    try:
        addresses = await api.async_reverse(
            lon=2.4764814791668925, lat=47.059424367067635, index="poi"
        )
        for address in addresses:
            logger.info("Address: %s", address)
    except AddressFrException as err:
        logger.error(err)
        return

    await api.async_close()


if __name__ == "__main__":
    asyncio.run(async_main())
