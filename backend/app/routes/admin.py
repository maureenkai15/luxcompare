"""
Admin / debug routes — v3.0
No auth in MVP. Prefix /admin and treat as internal.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import price_service, scraper_service
from app.services.tax_service import get_all_tax_configs
from app.utils.data_store import get_all_brands, get_all_countries, PRODUCTS

router = APIRouter()


@router.get("/tax-config")
def tax_config():
    """View current VAT/refund rules for all countries."""
    return get_all_tax_configs()


@router.get("/stats")
def stats():
    """Dataset overview."""
    return {
        "total_products": len(PRODUCTS),
        "brands":         get_all_brands(),
        "countries":      get_all_countries(),
        "total_brands":   len(get_all_brands()),
        "total_countries": len(get_all_countries()),
    }


@router.post("/reload-csv")
def reload_csv():
    """Hot-reload prices_override.csv without restarting the server."""
    msg = price_service.reload_csv()
    return {"message": msg}


class ScrapeRequest(BaseModel):
    scraper:    str = "mytheresa"
    url:        str = ""
    product_id: int = 1
    country:    str = "France"
    auto_url:   bool = True   # if True, build URL from product slug


@router.post("/scrape")
async def trigger_scrape(req: ScrapeRequest):
    """
    Trigger a scraper run. If auto_url=True and url is empty,
    builds the URL automatically from the product's mytheresa_slug.
    """
    url = req.url

    # Auto-build Mytheresa URL from product slug if not provided
    if req.scraper == "mytheresa" and req.auto_url and not url:
        built = scraper_service.get_mytheresa_url(req.product_id, req.country)
        if built:
            url = built
        else:
            raise HTTPException(
                status_code=400,
                detail="No mytheresa_slug for this product. Provide a URL manually."
            )

    if not url:
        raise HTTPException(status_code=400, detail="URL is required.")

    try:
        result = await scraper_service.run_scraper(
            scraper_name=req.scraper,
            url=url,
            product_id=req.product_id,
            country=req.country,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not result:
        raise HTTPException(status_code=502, detail="Scraper returned no data. Check logs.")

    return {
        "scraped":    True,
        "product_id": result.product_id,
        "country":    result.country,
        "currency":   result.currency,
        "price":      result.price,
        "source_url": result.source_url,
        "confidence": result.confidence,
        "note": "Price injected into ScrapedPriceProvider — next /compare call will use it.",
    }


@router.get("/scrape/url/{product_id}")
def get_scrape_url(product_id: int, country: str = "France"):
    """Preview the Mytheresa URL that would be scraped for a product."""
    url = scraper_service.get_mytheresa_url(product_id, country)
    if not url:
        raise HTTPException(status_code=404, detail="No Mytheresa slug for this product.")
    return {"product_id": product_id, "country": country, "url": url}


@router.get("/scrapers")
def list_scrapers():
    return {"scrapers": list(scraper_service.SCRAPERS.keys())}
