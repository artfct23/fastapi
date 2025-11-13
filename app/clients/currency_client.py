from decimal import Decimal
from typing import Dict

import httpx
from fastapi import HTTPException

from app.core.config import settings


class CurrencyClient:
    def __init__(self):
        self.base_url = settings.currency_api_url
        self.api_key = settings.currency_api_key
        self.timeout = 10.0

    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {"apikey": self.api_key}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if not data.get("success", False):
                    error_info = data.get("error", {})
                    error_message = error_info.get("info", "API request failed")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Currency API error: {error_message}"
                    )

                return data

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="External API timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"External API HTTP error: {e}"
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"External API error: {e}")

    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> Decimal:
        params = {"source": from_currency, "currencies": to_currency}
        data = await self._make_request("live", params)

        quote_key = f"{from_currency}{to_currency}"

        if quote_key not in data.get("quotes", {}):
            raise HTTPException(
                status_code=400,
                detail=f"Exchange rate for {from_currency}/{to_currency} not found"
            )

        return Decimal(str(data["quotes"][quote_key]))

    async def convert_currency(
            self,
            from_currency: str,
            to_currency: str,
            amount: Decimal
    ) -> Dict:
        exchange_rate = await self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * exchange_rate

        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": converted_amount.quantize(Decimal("0.01")),
            "exchange_rate": exchange_rate
        }

    async def get_currency_list(self) -> Dict[str, str]:
        data = await self._make_request("list")
        return data.get("currencies", {})


currency_client = CurrencyClient()
