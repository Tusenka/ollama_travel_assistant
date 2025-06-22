import os

from dto.search_parameters import SearchParameters
from services.booking.base import BookingClient
from services.booking.hotellook_api import HotelLookAPI
from services.utils import ServicesUtils


class HotelLookClient(BookingClient):
    def __init__(self, api_key: str):
        self.api = HotelLookAPI(api_key)

    async def search_hotels(self, params: SearchParameters) -> list:
        hotels_list = await self.api.search_hotels(params)
        hotels = []
        hotels.extend(
            {
                "hotelName": item.get("hotelName"),
                "priceAvg": item.get("priceFrom"),  # В API обычно поле priceFrom
                "hotel_id": item.get("hotelId"),
                "city_id": item.get("locationId"),
                "rate": int(item.get("stars", 0)),
            }
            for item in hotels_list
        )
        return hotels

    async def generate_hotel_link(
        self, hotel: dict, params: SearchParameters
    ) -> str:
        params = {
            "checkin": params.check_in,
            "checkout": params.check_out,
            "adults": params.adults,
            "children": params.children,
            "city_id": hotel["city_id"],
            "hotel_id": hotel["hotel_id"],
            "token": os.getenv("TRAVELPAYOUT_KEY"),
        }
        url = "https://search.hotellook.com/hotels"
        return ServicesUtils.create_link(url, params)

    async def generate_hotels_link(
        self, hotels: list, params: SearchParameters
    ) -> str:
        params = {
            "checkin": params.check_in,
            "checkout": params.check_out,
            "adults": params.adults,
            "children": params.children,
            "destination": params.city,
            "token": os.getenv("TRAVELPAYOUT_KEY"),
        }
        url = "https://search.hotellook.com/hotels"
        return ServicesUtils.create_link(url, params)
