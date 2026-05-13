"""
services/price_service.py

PriceProvider abstraction layer.

Current providers (in priority order):
  1. ScrapedPriceProvider  – returns prices from the in-memory scrape cache
                             (populated by scraper_service.py; empty by default)
  2. CsvPriceProvider      – reads from data/prices_override.csv if it exists
  3. StaticPriceProvider   – always-available fallback from data_store.py

Consumers call `get_product_prices(product_id)` and receive the best
available data without caring which provider answered.
"""

import csv
import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app.utils.data_store import PRODUCTS, get_product_by_id

logger = logging.getLogger(__name__)

# Path to optional CSV override file
_CSV_PATH = os.getenv("PRICE_CSV_PATH", "data/prices_override.csv")

# In-memory scrape cache  {product_id: {country: {currency, price}}}
_scrape_cache: Dict[int, Dict[str, Dict]] = {}


# ── Abstract interface ────────────────────────────────────────────────────────

class PriceProvider(ABC):
    """All price providers implement this interface."""

    @abstractmethod
    def get_prices(self, product_id: int) -> Optional[Dict[str, Dict]]:
        """Return {country: {currency, price}} or None if not available."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this provider has data to offer."""
        ...


# ── Concrete providers ────────────────────────────────────────────────────────

class StaticPriceProvider(PriceProvider):
    """Always-available fallback from the hardcoded data_store."""

    def get_prices(self, product_id: int) -> Optional[Dict[str, Dict]]:
        product = get_product_by_id(product_id)
        return product["prices"] if product else None

    def is_available(self) -> bool:
        return True


class CsvPriceProvider(PriceProvider):
    """
    Reads optional CSV overrides from data/prices_override.csv.

    Expected CSV columns:
        product_id, country, currency, price

    Example row:
        1,France,EUR,10500
    """

    def __init__(self, csv_path: str = _CSV_PATH):
        self._path = csv_path
        self._data: Dict[int, Dict[str, Dict]] = {}
        self._loaded = False
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self._path):
            return
        try:
            with open(self._path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pid = int(row["product_id"])
                    country = row["country"].strip()
                    self._data.setdefault(pid, {})[country] = {
                        "currency": row["currency"].strip().upper(),
                        "price": float(row["price"]),
                    }
            self._loaded = bool(self._data)
            logger.info("CsvPriceProvider: loaded %d product(s) from %s", len(self._data), self._path)
        except Exception as exc:
            logger.warning("CsvPriceProvider: failed to load %s — %s", self._path, exc)

    def reload(self) -> None:
        """Hot-reload the CSV (useful for admin endpoints)."""
        self._data.clear()
        self._loaded = False
        self._load()

    def get_prices(self, product_id: int) -> Optional[Dict[str, Dict]]:
        return self._data.get(product_id)

    def is_available(self) -> bool:
        return self._loaded


class ScrapedPriceProvider(PriceProvider):
    """
    Receives prices injected by scraper_service.py into the shared cache.
    Empty at startup — populated when scrapers run.
    """

    def get_prices(self, product_id: int) -> Optional[Dict[str, Dict]]:
        return _scrape_cache.get(product_id)

    def is_available(self) -> bool:
        return bool(_scrape_cache)


def inject_scraped_prices(product_id: int, country: str, currency: str, price: float) -> None:
    """Called by scraper_service to push prices into the shared cache."""
    _scrape_cache.setdefault(product_id, {})[country] = {
        "currency": currency,
        "price": price,
    }
    logger.info("Scraped price injected: product=%d %s/%s %.2f", product_id, country, currency, price)


# ── Provider chain ────────────────────────────────────────────────────────────

_providers: List[PriceProvider] = [
    ScrapedPriceProvider(),
    CsvPriceProvider(),
    StaticPriceProvider(),
]


def get_product_prices(product_id: int) -> tuple[Dict[str, Dict], str]:
    """
    Returns (prices_dict, source_label).
    Walks the provider chain and returns the first available result.
    """
    for provider in _providers:
        if provider.is_available():
            prices = provider.get_prices(product_id)
            if prices:
                source = type(provider).__name__.replace("PriceProvider", "").lower()
                return prices, source
    return {}, "none"


def get_all_products_with_source() -> List[Dict]:
    """Return product list annotated with which provider answered."""
    results = []
    for product in PRODUCTS:
        prices, source = get_product_prices(product["id"])
        results.append({
            **product,
            "prices": prices,
            "price_source": source,
        })
    return results


def reload_csv() -> str:
    """Reload CSV provider (for admin/debug endpoint)."""
    for p in _providers:
        if isinstance(p, CsvPriceProvider):
            p.reload()
            return "CSV reloaded"
    return "No CSV provider found"
