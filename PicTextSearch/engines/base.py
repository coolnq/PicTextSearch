from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from ..model.base import BaseSearchResponse
from ..network import RESP, HandOver

ResponseT = TypeVar("ResponseT")
T = TypeVar("T", bound=BaseSearchResponse[Any])


class BaseSearchEngine(HandOver, ABC, Generic[T]):
    def __init__(self, base_url: str, **request_kwargs):
        super().__init__(**request_kwargs)
        self.base_url = base_url

    @abstractmethod
    async def search(self, query: str, **kwargs) -> BaseSearchResponse:
        """Поиск картинок по текстовому запросу."""
        raise NotImplementedError

    async def _send_request(self, method: str, endpoint: str = "", url: str = "", **kwargs: Any) -> RESP:
        """Send an HTTP request and return the response.

        A utility method that handles both GET and POST requests to the search engine's API.

        Args:
            method (str): HTTP method, must be either 'get' or 'post' (case-insensitive).
            endpoint (str): API endpoint to append to the base URL. If empty, uses base_url directly.
            url (str): Full URL for the request. Overrides base_url and endpoint if provided.
            **kwargs (Any): Additional parameters for the request, such as:
                - params: URL parameters for GET requests
                - data: Form data for POST requests
                - files: Files to upload
                - headers: Custom HTTP headers
                - etc.

        Returns:
            RESP: A dataclass containing:
                - text: The response body as text
                - url: The final URL after any redirects
                - status_code: The HTTP status code

        Raises:
            ValueError: If an unsupported HTTP method is specified.
        """
        request_url = url or (f"{self.base_url}/{endpoint}" if endpoint else self.base_url)

        method = method.lower()
        if method == "get":
            # Files are not valid for GET requests
            kwargs.pop("files", None)
            return await self.get(request_url, **kwargs)
        elif method == "post":
            return await self.post(request_url, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
