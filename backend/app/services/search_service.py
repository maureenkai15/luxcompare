"""
Product search service — simple fuzzy/substring matching over the static dataset.
"""
from typing import List
from app.utils.data_store import PRODUCTS


def search_products(query: str) -> List[dict]:
    """
    Case-insensitive substring search across brand + product_name.
    Returns lightweight product cards (no prices) for the search results list.
    """
    q = query.strip().lower()
    if not q:
        return _to_cards(PRODUCTS)

    matched = [
        p for p in PRODUCTS
        if q in p["brand"].lower() or q in p["product_name"].lower()
    ]
    return _to_cards(matched)


def _to_cards(products: List[dict]) -> List[dict]:
    return [
        {
            "id": p["id"],
            "brand": p["brand"],
            "product_name": p["product_name"],
            "category": p["category"],
            "description": p.get("description", ""),
            "countries_available": list(p["prices"].keys()),
        }
        for p in products
    ]
