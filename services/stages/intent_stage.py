import os
from datetime import date
from logging import Logger

from dto.search_parameters import SearchParameters
from dto.search_parameters_intent import SearchParametersIntent
from services.llm.base import LLMClient
from services.time_utils import async_perf_counter
from services.utils import ServicesUtils

logger = Logger(__name__)


class IntentStage:
    def __init__(self, llm_clients: list[LLMClient]):
        self.llm_clients = llm_clients
        self.system_prompt = ServicesUtils.load_prompt(
            "%s/intent_prompt.txt" % os.getenv("SYSTEM_PROMPTS_FILEPATH")
        )

    @async_perf_counter
    async def analyze_and_extract_params(
        self, history: list, lang="en"
    ) -> SearchParametersIntent:
        err = None

        for llm_client in self.llm_clients:
            try:
                response = await llm_client.extract_rag(
                    history=history, system_prompt=self.system_prompt, lang=lang
                )
                if "extracted_params" in response:
                    params: SearchParameters = self._try_to_extract_params(
                        response["extracted_params"]
                    )
                    response["extracted_params"] = params
                return SearchParametersIntent.model_validate(response)
            except BaseException as e:
                logger.warning(
                    f"An exception {e} has been occurred for search params analyze for {llm_client}"
                )
                err = e
        raise err

    @staticmethod
    def _try_to_extract_params(extracted_params: dict) -> SearchParameters | None:
        try:
            parameters = SearchParameters.model_validate(extracted_params)

            # checkin_year = date.fromisoformat(parameters.check_in).year
            # checkout_year = date.fromisoformat(parameters.check_out).year
            #
            # if checkin_year < date.today().year or checkout_year < date.today().year:
            #     parameters.check_in = parameters.check_in.replace(
            #         str(checkin_year), str(date.today().year)
            #     )
            #     parameters.check_out = parameters.check_out.replace(
            #         str(checkin_year), str(date.today().year)
            #     )
            #
            # if date.fromisoformat(parameters.check_in) < date.today():
            #     logger.warning(
            #         f"Warning! check in date {parameters.check_in} is less then today, manually set today date"
            #     )
            #     check_diff = date.fromisoformat(
            #         parameters.check_out
            #     ) - date.fromisoformat(parameters.check_in)
            #     parameters.check_in = date.today().isoformat()
            #     parameters.check_out = (date.today() + check_diff).isoformat()

            return parameters
        except BaseException as e:
            logger.warning(
                f"Warning! An exception {e} has been occurred while analysing extracted params, perhaps incomplete params"
            )
            return None
