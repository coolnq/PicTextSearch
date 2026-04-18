from ..model import YandexResponse
from .base import BaseSearchEngine


class Yandex(BaseSearchEngine[YandexResponse]):
    def __init__(self, base_url: str = "https://yandex.com/images/search", **kwargs):
        super().__init__(base_url, **kwargs)

    async def search(self, query: str, **kwargs) -> YandexResponse:
        params = {
            "text": query,
            "p": 0,
            "nomisspell": 1,
            "source": "search"
        }
        resp = await self.get(self.base_url, params=params)
        return YandexResponse(resp.text, str(resp.url))
