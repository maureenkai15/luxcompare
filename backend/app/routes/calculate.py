from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.price_calculator import calculate_country_price
from app.services import fx_service

router = APIRouter()


class CalculateRequest(BaseModel):
    country:     str   = Field(..., example="France")
    currency:    str   = Field(..., example="EUR")
    local_price: float = Field(..., gt=0, example=10300)


@router.post("")
async def calculate(req: CalculateRequest):
    """
    Calculate the final SGD landed cost for an arbitrary local price.
    Uses live FX rates. Useful for items not yet in the product catalogue.
    """
    try:
        result = await calculate_country_price(
            country=req.country,
            local_price=req.local_price,
            currency=req.currency,
        )
        result["fx_meta"] = fx_service.get_cache_meta()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
