import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class ServicesUtils:
    @staticmethod
    def load_prompt(filepath: str) -> str:
        prompt_path = Path(filepath)
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file {filepath} not found.")
        return prompt_path.read_text(encoding="utf-8")

    @staticmethod
    def create_link(url, params):
        url_parts = list(urlparse(url))
        # Извлекаем существующие параметры
        query_params = parse_qs(url_parts[4])

        # Добавляем или обновляем параметры
        query_params.update(
            {
                "checkIn": params["checkin"],  # Формат даты: '2025-02-01'
                "checkOut": params["checkout"],  # Формат даты: '2025-02-10'
                "adults": params["adults"] if params["adults"] <= 4 else "4",
                "children": "7" if params["children"] >= 1 else "",
                "childrens": "7" if params["children"] >= 2 else "",
                "childrenss": "7" if params["children"] >= 3 else "",
                "cityId": params.get("city_id", ""),
                "currency": "rub",
                "hotelId": params.get("hotel_id", ""),
                "destination": params.get("destination", ""),
                "language": "ru",
                "marker": os.getenv("MARKER"),
                "token": params.get("token", ""),
            }
        )

        # Кодируем параметры обратно в строку
        url_parts[4] = urlencode(query_params, doseq=True)

        # Собираем URL обратно
        return urlunparse(url_parts)
