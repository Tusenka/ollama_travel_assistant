from abc import ABC, abstractmethod

from dto.search_parameters import SearchParameters


class BookingClient(ABC):
    @abstractmethod
    async def search_apartments(self, params: SearchParameters) -> list:
        raise NotImplementedError()

    @abstractmethod
    async def generate_apartment_link(
        self, apartment: dict, params: SearchParameters
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def generate_apartments_link(
        self, apartments: list, params: SearchParameters
    ) -> str:
        raise NotImplementedError()
