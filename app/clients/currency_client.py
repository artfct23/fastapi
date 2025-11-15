from decimal import Decimal
from typing import Dict
from app.core.base_client import BaseClient
from app.core.config import settings


class CurrencyClient(BaseClient):

    def __init__(self):
        super().__init__(
            base_url=settings.currency_api_url,
            timeout=10.0
        )

    async def get_exchange_rate(
            self,
            from_currency: str,
            to_currency: str
    ) -> Decimal:
        response = await self.make_request(
            method="GET",
            endpoint=from_currency
        )
        data = response.json()
        rates = data.get("rates", {})

        if to_currency not in rates:
            raise ValueError(f"Currency {to_currency} not found")

        return Decimal(str(rates[to_currency]))

    async def convert_currency(
            self,
            from_currency: str,
            to_currency: str,
            amount: Decimal
    ) -> Dict[str, Decimal]:

        exchange_rate = await self.get_exchange_rate(
            from_currency,
            to_currency
        )

        converted_amount = amount * exchange_rate

        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": converted_amount.quantize(Decimal("0.01")),
            "exchange_rate": exchange_rate
        }

    async def get_currency_list(self) -> Dict[str, str]:
        return {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "RUB": "Russian Ruble",
            "JPY": "Japanese Yen",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "AUD": "Australian Dollar",
        }

currency_client = CurrencyClient()

