from pydantic import BaseModel, StrictStr, StrictBool

from dto.search_parameters import SearchParameters


class SearchParametersIntent(BaseModel):
    communicate: StrictBool
    response: StrictStr
    extracted_params: SearchParameters | None = None
    # TBD: custom typing
    lang: StrictStr = "ru"
