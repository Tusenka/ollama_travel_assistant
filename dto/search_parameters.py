from typing import Optional

from pydantic import BaseModel, StrictStr, NonNegativeInt


class SearchParameters(BaseModel):
    check_in: str
    check_out: str
    adults: NonNegativeInt | None = 2
    children: NonNegativeInt | None = 0
    rooms: NonNegativeInt | None = 1
    hotel_name: StrictStr | None = None
    city: StrictStr | None = None
    hotel_ids: list | None = None
    price_min: float | None = None
    price_max: float | None = None
    quality: StrictStr | None = None
