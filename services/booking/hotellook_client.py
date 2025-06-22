import os

from dto.search_parameters import SearchParameters
from services.booking.base import BookingClient
from services.booking.hotellook_api import HotelLookAPI
from services.utils import ServicesUtils


class HotelLookClient(BookingClient):
    def __init__(self, api_key: str):
        self.api = HotelLookAPI(api_key)

    async def search_apartments(self, params: SearchParameters) -> list:
        apartments_list = await self.api.search_apartments(params)
        apartments = []
        apartments.extend(
            {
                "apartmentName": item.get("hotelName"),
                "priceAvg": item.get("priceFrom"),  # В API обычно поле priceFrom
                "apartment_id": item.get("hotelId"),
                "city_id": item.get("locationId"),
                "rate": int(item.get("stars", 0)),
            }
            for item in apartments_list
        )
        return apartments

    async def generate_apartment_link(
        self, apartment: dict, params: SearchParameters
    ) -> str:
        params = {
            "checkin": params.check_in,
            "checkout": params.check_out,
            "adults": params.adults,
            "children": params.children,
            "city_id": apartment["city_id"],
            "hotel_id": apartment["hotel_id"],
            "token": os.getenv("TRAVELPAYOUT_KEY"),
        }
        url = "https://search.hotellook.com/hotels"
        return ServicesUtils.create_link(url, params)

    async def generate_apartments_link(
        self, apartments: list, params: SearchParameters
    ) -> str:
        params = {
            "checkin": params.check_in,
            "checkout": params.check_out,
            "adults": params.adults,
            "children": params.children,
            "destination": params.city,
            "token": os.getenv("TRAVELPAYOUT_KEY"),
        }
        url = "https://search.apartmentlook.com/apartments"
        return ServicesUtils.create_link(url, params)
