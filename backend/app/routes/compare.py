from fastapi import APIRouter, HTTPException
from app.services.price_calculator import compare_all_countries
from app.utils.data_store import get_product_by_id

router = APIRouter()


@router.get("/{product_id}")
async def compare(product_id: int):
    """
    Return a full country-by-country price comparison for a product.

    Includes live FX rates, VAT-adjusted prices, import GST, savings vs Singapore,
    a natural-language recommendation, and FX metadata (source, timestamp).
    """
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    return await compare_all_countries(product)
