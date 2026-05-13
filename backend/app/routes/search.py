from fastapi import APIRouter, Query
from app.services.search_service import search_products

router = APIRouter()


@router.get("")
def search(q: str = Query(default="", description="Brand or product name to search")):
    """
    Search luxury products by brand or product name.

    - **q**: search query string (e.g. "Chanel", "Lady Dior", "Birkin")
    """
    results = search_products(q)
    return {"query": q, "count": len(results), "results": results}
