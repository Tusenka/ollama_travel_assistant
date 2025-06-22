import os
from logging import Logger

from services.llm.base import LLMClient
from services.utils import ServicesUtils

logger = Logger(__name__)


class ApartmentHintStage:
    def __init__(self, llm_clients: list[LLMClient]):
        self.llm_clients = llm_clients
        self.system_prompt = ServicesUtils.load_prompt(
            f'{os.getenv("SYSTEM_PROMPTS_FILEPATH")}/apartments_prompt.txt'
        )

    async def generate(self, apartments_list: list, history: list, lang: str) -> dict:
        apartments_text = "\n".join(
            f"- Apartment name:{apartment['apartmentName']}; PriceAvg: ${round(apartment['priceAvg'])}; Hotel id: {apartment['apartment_id']}; City id: {apartment['city_id']}; PriceAvg: ${round(apartment['priceAvg'])};"
            for apartment in apartments_list
        )
        new_history = history["messages"] + [
            {
                "role": "assistant",
                "content": f"Here is the list of available apartments:\n{apartments_text}",
            },
            {"role": "user", "content": f"Please recommend apartments. Say {lang}"},
        ]
        err = None
        for llm_client in self.llm_clients:
            try:
                result = await llm_client.generate_response(
                    history=new_history, system_prompt=self.system_prompt
                )
                if "apartments" not in result:
                    raise Exception(result["response"])
                break
            except Exception as e:
                logger.warning(
                    f"An exception {e} has been occurred for apartments intent analyze for {llm_client}"
                )
                err = e
        else:
            raise err
        return result
