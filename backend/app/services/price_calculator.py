"""
services/price_calculator.py  (upgraded)

Replaces hardcoded FX rates and VAT values with:
  - fx_service  → live rates (with fallback)
  - tax_service → rule-based VAT config

All public functions are now async because FX lookup is async.
"""

from typing import Dict

from app.services import fx_service
from app.services.tax_service import (
    SG_IMPORT_GST_RATE,
    calculate_vat_refund,
    get_tax_config,
)
from app.services.price_service import get_product_prices
from app.utils.data_store import get_product_by_id


async def calculate_country_price(
    country: str,
    local_price: float,
    currency: str,
) -> Dict:
    """
    All-in SGD landed cost for buying in `country`.
    Returns a full breakdown dict for transparent display.
    """
    tax = get_tax_config(country)
    exchange_rate = await fx_service.get_rate(currency)

    vat_refund_local = calculate_vat_refund(country, local_price)
    price_after_refund_local = round(local_price - vat_refund_local, 2)
    price_after_refund_sgd = round(price_after_refund_local * exchange_rate, 2)

    if country == "Singapore":
        import_gst_sgd = 0.0
        final_price_sgd = round(local_price, 2)
    else:
        import_gst_sgd = round(price_after_refund_sgd * SG_IMPORT_GST_RATE, 2)
        final_price_sgd = round(price_after_refund_sgd + import_gst_sgd, 2)

    return {
        "country": country,
        "currency": currency,
        "local_price": local_price,
        "vat_refund_rate": tax["refund_rate"],
        "vat_refund_local": vat_refund_local,
        "price_after_refund_local": price_after_refund_local,
        "exchange_rate_to_sgd": exchange_rate,
        "price_after_refund_sgd": price_after_refund_sgd,
        "import_gst_sgd": import_gst_sgd,
        "final_price_sgd": final_price_sgd,
    }


async def compare_all_countries(product: Dict) -> Dict:
    """
    Compare all countries for a product using the price_service provider chain.
    Returns full breakdown + recommendation + FX metadata.
    """
    prices, price_source = get_product_prices(product["id"])
    if not prices:
        prices = product.get("prices", {})
        price_source = "static"

    results = []
    sg_price = None

    for country, price_info in prices.items():
        breakdown = await calculate_country_price(
            country=country,
            local_price=price_info["price"],
            currency=price_info["currency"],
        )
        results.append(breakdown)
        if country == "Singapore":
            sg_price = breakdown["final_price_sgd"]

    results.sort(key=lambda x: x["final_price_sgd"])

    for r in results:
        r["savings_vs_sg"] = round((sg_price or 0) - r["final_price_sgd"], 2)

    cheapest = results[0]
    fx_meta = fx_service.get_cache_meta()

    return {
        "product_id":         product["id"],
        "brand":              product["brand"],
        "product_name":       product["product_name"],
        "category":           product["category"],
        "description":        product.get("description", ""),
        "comparisons":        results,
        "recommendation":     _build_recommendation(cheapest, sg_price),
        "cheapest_country":   cheapest["country"],
        "cheapest_final_sgd": cheapest["final_price_sgd"],
        "price_source":       price_source,
        "fx_meta": {
            "source":      fx_meta["source"],
            "live_ok":     fx_meta["live_ok"],
            "fetched_at":  fx_meta["fetched_at_iso"],
            "age_seconds": fx_meta["age_seconds"],
        },
    }


def _build_recommendation(cheapest: Dict, sg_price) -> str:
    country = cheapest["country"]
    final   = cheapest["final_price_sgd"]
    savings = cheapest.get("savings_vs_sg", 0)

    if country == "Singapore":
        return (
            f"Singapore is already the most cost-effective option at S${final:,.0f} — "
            f"no import hassle, no currency risk."
        )
    if savings > 0:
        return (
            f"{country} is currently the cheapest country to purchase this item, "
            f"with an estimated all-in cost of S${final:,.0f} — "
            f"saving you approximately S${savings:,.0f} compared to buying in Singapore."
        )
    return (
        f"Buying in {country} results in an estimated final cost of S${final:,.0f} "
        f"after VAT refund, currency conversion, and Singapore import GST."
    )
