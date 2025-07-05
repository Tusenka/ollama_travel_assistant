import os
from logging import Logger

from services.llm.base import LLMClient
from services.time_utils import async_perf_counter
from services.utils import ServicesUtils

logger = Logger(__name__)


class HotelHintStage:
    def __init__(self, llm_clients: list[LLMClient]):
        self.llm_clients = llm_clients
        self.system_prompt = ServicesUtils.load_prompt(
            f'{os.getenv("SYSTEM_PROMPTS_FILEPATH")}/hotels_prompt.txt'
        )

    @async_perf_counter
    async def generate(self, hotels_list: list, history: dict, lang: str) -> dict:
        hotels_text = "\n".join(
            f"- Hotel name:{hotel['hotelName']}; PriceAvg: ${round(hotel['priceAvg'])}; Hotel id: {hotel['hotel_id']}; City id: {hotel['city_id']}; PriceAvg: ${round(hotel['priceAvg'])};"
            for hotel in hotels_list
        )
        new_history = history["messages"] + [
            {
                "role": "assistant",
                "content": f"Here is the list of available hotels:\n{hotels_text}",
            },
            {"role": "user", "content": f"Please recommend hotel from the list. Say in {lang}"},
        ]
        err = None
        for llm_client in self.llm_clients:
            try:
                result = await llm_client.generate_response(
                    history=new_history, system_prompt=self.system_prompt
                )
                if "hotels" not in result:
                    raise Exception(result)
                break
            except Exception as e:
                logger.warning(
                    f"An exception {e} has been occurred for hotels intent analyze for {llm_client}"
                )
                err = e
        else:
            raise err
        return result
