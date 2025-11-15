"""
Base HTTP client for all API integrations.
Handles common request/response logic.
"""

import httpx
from typing import Any, Optional
from app.core.config import settings


class BaseClient:
    """Base client for all external API integrations."""

    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Initialize base client.

        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout

    async def make_request(
            self,
            method: str,
            endpoint: str,
            **kwargs: Any
    ) -> httpx.Response:
        """
        Make HTTP request to external API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for httpx.request

        Returns:
            httpx.Response object (not parsed JSON!)

        Raises:
            httpx.RequestError: If request fails
        """
        url = f"{self.base_url}/{endpoint}".rstrip("/")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response  # ✅ Возвращаем Response, не JSON!

        except httpx.RequestError as e:
            raise httpx.RequestError(f"API request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"HTTP error {e.response.status_code}: {e.response.text}",
                request=e.request,
                response=e.response
            )
