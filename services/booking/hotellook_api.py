from typing import Dict, Optional
import httpx
from pydantic import BaseModel

from dto.search_parameters import SearchParameters


class HotelLookAPI:
    BASE_URL = "https://engine.hotellook.com/api/v2"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}{endpoint}"
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise Exception(f"HotelLook API request failed: {str(e)}")

    async def search_hotels(self, params: SearchParameters) -> dict:
        params = {
            "location": params.city,
            "checkIn": params.check_in,
            "checkOut": params.check_out,
            "adults": min(params.adults, 4),
            "limit": 100,
            "currency": "rub",
            "token": self.api_key,
        }
        return await self._make_request("/cache.json", params)
