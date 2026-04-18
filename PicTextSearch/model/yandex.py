import json
import re
from typing import Any, Dict

from ddgs.utils import json_loads
from pyquery import PyQuery
from typing_extensions import override

from .base import BaseSearchItem, BaseSearchResponse
from ..exceptions import ParsingError
from ..utils import parse_html, deep_get


class YandexItem(BaseSearchItem):
    def __init__(self, data: dict[str, Any], **kwargs: Any):
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: Dict[str, Any], **kwargs):
        viewer_data = data.get("viewerData", {})

        # Заголовок
        self.title = viewer_data.get("snippet", {}).get("title", "")

        # Прямая ссылка на оригинальное изображение
        self.url = data.get("origUrl", "")

        # Миниатюра (часто начинается с //) -> добавляем https:
        thumb = data.get("image", "")
        if thumb.startswith("//"):
            thumb = "https:" + thumb
        self.thumbnail = thumb

        # Оригинальные размеры
        self.size = f"{data.get("origWidth", 0)}x{data.get("origHeight", 0)}"

        self.content: str = viewer_data.get("snippet", {}).get("text", "")

        # Домен источника
        self.source = data.get("snippet", {}).get("domain", "")


class YandexResponse(BaseSearchResponse[YandexItem]):
    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: str, **kwargs):
        # Ищем элемент с id, начинающимся на ImagesApp-
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        data_div = data.find('div.Root[id^="ImagesApp-"]')
        data_state = data_div.attr("data-state")

        if not data_state:
            raise ParsingError(
                message="Failed to find critical DOM attribute 'data-state'",
                engine="yandex",
                details="This usually indicates a change in the page structure or an unexpected response.",
            )

        data_json = json_loads(str(data_state))
        if entities := deep_get(data_json, "initialState.serpList.items.entities"):
            self.raw: list[YandexItem] = [YandexItem(entity) for entity in list(entities.values())]
        else:
            raise ParsingError(
                message="Failed to extract search results from 'data-state'",
                engine="yandex",
                details="This usually indicates a change in the page structure or an unexpected response.",
            )
