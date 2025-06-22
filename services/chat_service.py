import random
import logging
from typing import List, Tuple, Union

from dto.search_parameters import SearchParameters
from dto.search_parameters_intent import SearchParametersIntent
from services.booking.base import BookingClient
from services.stages.intent_stage import IntentStage
from services.stages.hotel_hint_stage import HotelHintStage
from services.time_utils import async_perf_counter

logger = logging.getLogger("ChatService")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class ChatService:
    def __init__(self, llm_clients: List, booking_clients: List[BookingClient]):
        assert booking_clients

        self.booking_clients = booking_clients
        self.rag_stage = IntentStage(llm_clients)
        self.hint_stage = HotelHintStage(llm_clients)

    @async_perf_counter
    async def handle_user_message(self, history: List[dict]) -> str:
        intent_result = await self.rag_stage.analyze_and_extract_params(history)

        if not intent_result.extracted_params:
            return intent_result.response

        return await self._get_hotels(
            params=intent_result.extracted_params,
            full_response=intent_result.response,
            history=history,
            intent_result=intent_result,
        )
    @async_perf_counter
    async def _get_hotels(
        self,
        params: SearchParameters,
        full_response: str,
        history: List[dict],
        intent_result: SearchParametersIntent,  # You can replace 'object' with a specific type if available
    ) -> str:
        current_booking_client, hotels_list = (
            await self._get_hotels_list_from_client(params)
        )
        result: dict = await self.hint_stage.generate(
            hotels_list, history, intent_result.lang
        )

        hotels_intro: str = result.get("response", "")
        response: str = f"{full_response}\n\n{hotels_intro}\n\n"
        idx = 0
        best_hotels: List[dict] = result.get("hotels", [])
        response+="<br><br>"
        for hotel in best_hotels:
            idx += 1
            response += (
                f"{idx}. {hotel['text']} - ₽{round(hotel['priceAvg'])} Руб."
                "<br>"
                f"<a href='{await current_booking_client.generate_hotel_link(hotel, params)}' target='_blank' rel='noopener noreferrer'>{result['link_text']}</a>\n\n"
                "<br><br>"
            )
        response += await self._show_extra_hotels(
            current_booking_client, params, hotels_list, result
        )

        return response

    @async_perf_counter
    async def _get_hotels_list_from_client(
        self, params: SearchParameters
    ) -> Tuple[BookingClient, List[dict]]:
        hotels_list: List[dict] = []
        current_booking_client: BookingClient = self.booking_clients[0]

        for booking_client in self.booking_clients:
            try:
                hotels_list = await booking_client.search_hotels(params)
                if hotels_list:
                    current_booking_client = booking_client
                    break
                else:
                    logger.warning(
                        "Warning! Got an empty list of hotels from %s",
                        booking_client,
                    )
            except Exception as e:
                logger.warning(
                    "Warning! Exception while trying to get list of hotels from %s: %s",
                    booking_client,
                    e,
                )
        logger.warning(
            "Got an hotel list with count %d: %s for booking client %s",
            len(hotels_list),
            hotels_list,
            current_booking_client,
        )

        return current_booking_client, hotels_list

    @staticmethod
    @async_perf_counter
    async def _show_extra_hotels(
        current_booking_client: BookingClient,
        params: SearchParameters,
        hotels_list: List[dict],
        result: dict,
    ) -> str:

        if not hotels_list:
            return ""

        return (
            f"<a class='button' href='"
            f"{await current_booking_client.generate_hotels_link(hotels_list, params)}' "
            f"target='_blank' rel='noopener noreferrer'>{result.get('show_all_variants_text')}...</a>"
        )
