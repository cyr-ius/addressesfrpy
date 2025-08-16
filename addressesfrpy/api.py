"""API for querying French addresses using the address fr."""

import logging
from typing import Any

from addressesfrpy.consts import API_BASE_URL

from .auth import HTTPRequest, HttpRequestError
from .exceptions import AddressFrException, AddressNotFound

_LOGGER = logging.getLogger(__name__)


class AddressFr(HTTPRequest):
    """Class to handle French addresses."""

    async def async_search(
        self, query: str, limit: int = 10, **kwargs: Any
    ) -> list[dict[str, Any]]:
        """Query the addresses.

        Args:
            q (str): The search query, e.g., "Paris".
            autocomplete (bool): If True, returns autocomplete suggestions.
            index (str): The index type to search in, e.g., "poi" or "poi,parcel".
                Possible values are "poi", "address", "parcel".
            limit (int): The maximum number of results to return, default is 10.
            lat (float): Latitude of the location to search around.
            lon (float): Longitude of the location to search around.
            returntruegeometry (bool): If True, returns the true geometry of the address.
            postcode (str): The postcode to filter the results.
            citycode (str): The city code to filter the results.
            type (str): The type of address to search for, e.g., "street", "city", etc.
            city (str): The city name to filter the results.
            category (str): The category of the address, e.g., "restaurant", "school", etc.
            departmentcode (str): The department code to filter the results.
            municipalitycode (str): The municipality code to filter the results.
            oldmunicipalitycode (str): The old municipality code to filter the results.
            districtcode (str): The district code to filter the results.
            section (str): The section code to filter the results.
            number (str): The house number to filter the results.
            sheet (str): The sheet number to filter the results.
        Raises:
            AddressNotFound: If no addresses are found for the given query.

        Returns:
            A list of addresses found for the given query.

        Docs:
            https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage
        """

        try:
            addresses = await self.async_request(
                path=API_BASE_URL + "/search",
                params={
                    "q": query,
                    "limit": limit,
                    **kwargs,
                },
            )
        except HttpRequestError as error:
            _LOGGER.error("Failed to query address: %s", error)
            raise AddressNotFound("Address not found.") from error

        return self._check_response(addresses)

    async def async_reverse(self, **kwargs: Any) -> list[dict[str, Any]]:
        """Reverse geocode a location to find the address.

        Args:
            lon (float): Longitude of the location.
            lat (float): Latitude of the location.
            searchgeom (str): The type of geometry to return, e.g., "polygon",
            index (str): The index type to search in, e.g., "poi" or "poi,parcel".
                Possible values are "poi", "address", "parcel".
            limit (int): The maximum number of results to return, default is 10.
            returntruegeometry (bool): If True, returns the true geometry of the address.
            postcode (str): The postcode to filter the results.
            citycode (str): The city code to filter the results.
            type (str): The type of address to search for, e.g., "street", "city", etc.
            city (str): The city name to filter the results.
            category (str): The category of the address, e.g., "restaurant", "school", etc.
            departmentcode (str): The department code to filter the results.
            municipalitycode (str): The municipality code to filter the results.
            oldmunicipalitycode (str): The old municipality code to filter the results.
            districtcode (str): The district code to filter the results.
            section (str): The section code to filter the results.
            number (str): The house number to filter the results.
            sheet (str): The sheet number to filter the results.
        Raises:
            AddressNotFound: If no addresses are found for the given coordinates.

        Returns:
            A list of addresses found for the given coordinates.

        Docs:
            https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage
        """
        try:
            addresses = await self.async_request(
                path=API_BASE_URL + "/reverse",
                params={**kwargs},
            )
        except HttpRequestError as error:
            _LOGGER.error("Failed to query address: %s", error)
            raise AddressNotFound("Address not found.") from error

        return self._check_response(addresses)

    def _check_response(self, response: Any) -> Any:
        """Check the response for errors."""
        if response and isinstance(response, dict) and "features" in response:
            response = response["features"]
            if not response:
                raise AddressNotFound("No addresses found for the given query.")
            return response
        if not response or not isinstance(response, dict):
            raise AddressFrException("Invalid response from address service.")
        if "error" in response:
            raise AddressFrException(f"Error in response: {response['error']}")
        if "features" not in response or not response["features"]:
            raise AddressFrException("No features found in the response.")

    async def async_close(self) -> None:
        """Close the HTTP session."""
        await super().async_close()
