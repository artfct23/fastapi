from decimal import Decimal
from typing import Dict
from pydantic import BaseModel, Field, ConfigDict


class CurrencyConvertRequest(BaseModel):
    from_currency: str = Field(..., min_length=3, max_length=3)
    to_currency: str = Field(..., min_length=3, max_length=3)
    amount: Decimal = Field(default=Decimal("1.0"), gt=0)


class ExchangeRateResponse(BaseModel):
    from_currency: str
    to_currency: str
    exchange_rate: Decimal

    model_config = ConfigDict(json_encoders={Decimal: str})


class ConversionResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: Decimal
    converted_amount: Decimal
    exchange_rate: Decimal

    model_config = ConfigDict(json_encoders={Decimal: str})


class CurrencyListResponse(BaseModel):
    currencies: Dict[str, str]
