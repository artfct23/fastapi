from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.db.user import User
from app.models.schemas.currency import (
    CurrencyConvertRequest,
    ConversionResponse,
    ExchangeRateResponse,
    CurrencyListResponse,
)
from app.clients.currency_client import currency_client

router = APIRouter(prefix="/currency", tags=["Currency"])


@router.get("/exchange", response_model=ExchangeRateResponse)
async def get_exchange_rate(
    from_currency: str,
    to_currency: str,
    current_user: User = Depends(get_current_user),
):
    try:
        rate = await currency_client.get_exchange_rate(
            from_currency.upper(),
            to_currency.upper()
        )
        return ExchangeRateResponse(
            from_currency=from_currency.upper(),
            to_currency=to_currency.upper(),
            exchange_rate=rate
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail="Currency API error")


@router.post("/convert", response_model=ConversionResponse)
async def convert_currency(
    conversion: CurrencyConvertRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        result = await currency_client.convert_currency(
            conversion.from_currency.upper(),
            conversion.to_currency.upper(),
            conversion.amount
        )
        return ConversionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail="Currency API error")


@router.get("/list", response_model=CurrencyListResponse)
async def get_currency_list(
    current_user: User = Depends(get_current_user),
):
    currencies = await currency_client.get_currency_list()
    return CurrencyListResponse(currencies=currencies)
