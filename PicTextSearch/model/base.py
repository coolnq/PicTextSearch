from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, List

T = TypeVar("T")


class BaseSearchItem(ABC):
    """Одна картинка в результатах поиска."""

    def __init__(self, data: Any, **kwargs):
        self.origin = data
        self.title: str = ""
        self.url: str = ""  # прямая ссылка на изображение
        self.thumbnail: str = ""  # миниатюра
        self.size: str = ""
        self.source: str = ""  # домен-источник
        self._parse_data(data, **kwargs)

    @abstractmethod
    def _parse_data(self, data: Any, **kwargs): ...


class BaseSearchResponse(ABC, Generic[T]):
    def __init__(self, resp_data: Any, resp_url: str, **kwargs):
        self.origin = resp_data
        self.url = resp_url
        self.raw: List[T] = []
        self._parse_response(resp_data, **kwargs)

    @abstractmethod
    def _parse_response(self, resp_data: Any, **kwargs): ...
