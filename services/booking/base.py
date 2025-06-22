from abc import ABC, abstractmethod

from dto.search_parameters import SearchParameters


class BookingClient(ABC):
    @abstractmethod
    async def search_hotels(self, params: SearchParameters) -> list:
        raise NotImplementedError()

    @abstractmethod
    async def generate_hotel_link(
        self, hotel: dict, params: SearchParameters
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def generate_hotels_link(
        self, hotels: list, params: SearchParameters
    ) -> str:
        raise NotImplementedError()
