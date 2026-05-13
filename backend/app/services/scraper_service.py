"""
services/scraper_service.py — v3.0

Scraper framework with real Mytheresa implementation using Playwright.

Architecture:
  BaseScraper        – abstract interface every scraper must implement
  MytheresaScraper   – real Playwright scraper for mytheresa.com
  DemoScraper        – mock scraper for testing without a browser
  FarfetchScraper    – stub (ready to implement)

Usage:
  POST /admin/scrape  {"scraper": "mytheresa", "url": "...", "product_id": 1, "country": "France"}

Install:
  pip install playwright
  playwright install chromium
"""

import asyncio
import logging
import re
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from app.services.price_service import inject_scraped_prices

logger = logging.getLogger(__name__)

# Currency symbol → ISO code mapping
CURRENCY_SYMBOLS: dict[str, str] = {
    "€": "EUR",
    "£": "GBP",
    "¥": "JPY",
    "₩": "KRW",
    "$": "USD",
    "S$": "SGD",
    "AED": "AED",
}

# Country → currency code
COUNTRY_CURRENCIES: dict[str, str] = {
    "France": "EUR",
    "Italy": "EUR",
    "Germany": "EUR",
    "Spain": "EUR",
    "Japan": "JPY",
    "Singapore": "SGD",
    "UK": "GBP",
    "USA": "USD",
    "South Korea": "KRW",
    "UAE": "AED",
}


@dataclass
class ScrapedPrice:
    product_id: int
    country: str
    currency: str
    price: float
    source_url: str
    confidence: float   # 0.0–1.0


# ── Base class ────────────────────────────────────────────────────────────────

class BaseScraper(ABC):
    name: str = "base"

    @abstractmethod
    async def fetch_price(self, url: str, product_id: int, country: str) -> Optional[ScrapedPrice]:
        """Fetch and parse price from a product URL."""
        ...

    async def run(self, url: str, product_id: int, country: str) -> Optional[ScrapedPrice]:
        try:
            result = await self.fetch_price(url, product_id, country)
            if result:
                inject_scraped_prices(
                    product_id=result.product_id,
                    country=result.country,
                    currency=result.currency,
                    price=result.price,
                )
                logger.info("[%s] scraped %s %s %.2f for product %d",
                            self.name, result.country, result.currency,
                            result.price, result.product_id)
            return result
        except Exception as exc:
            logger.error("[%s] scrape failed: %s", self.name, exc)
            return None


# ── Mytheresa Scraper (Playwright) ────────────────────────────────────────────

class MytheresaScraper(BaseScraper):
    """
    Real scraper for mytheresa.com using Playwright headless Chrome.

    Mytheresa renders prices via JavaScript, so a real browser is needed.
    Prices are found in:
      1. JSON-LD structured data (most reliable)
      2. data-price attribute on the buy button
      3. Visible price element as fallback

    The site serves EUR prices by default. To get prices in other
    currencies, the URL must include the correct region parameter
    or the site must be accessed from that country's IP.

    Requires: pip install playwright && playwright install chromium
    """

    name = "mytheresa"
    base_url = "https://www.mytheresa.com"

    # Selectors to try in order (Mytheresa changes these occasionally)
    PRICE_SELECTORS = [
        '[data-testid="price"]',
        '.product__price',
        '.price__current',
        '[class*="Price_price"]',
        'span[class*="price"]',
    ]

    async def fetch_price(self, url: str, product_id: int, country: str) -> Optional[ScrapedPrice]:
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            logger.error(
                "Playwright not installed. Run: pip install playwright && playwright install chromium"
            )
            return None

        currency = COUNTRY_CURRENCIES.get(country, "EUR")

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                ],
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                locale="en-GB",
            )

            page = await context.new_page()

            try:
                logger.info("[mytheresa] Loading %s", url)
                await page.goto(url, wait_until="networkidle", timeout=30000)

                # Accept cookie banner if present
                try:
                    await page.click('[data-testid="uc-accept-all-button"]', timeout=3000)
                    await asyncio.sleep(1)
                except Exception:
                    pass

                # Wait for price to appear
                await page.wait_for_selector(
                    ", ".join(self.PRICE_SELECTORS),
                    timeout=10000
                )

                price, confidence = await self._extract_price(page, url)

                if price:
                    return ScrapedPrice(
                        product_id=product_id,
                        country=country,
                        currency=currency,
                        price=price,
                        source_url=url,
                        confidence=confidence,
                    )

            except Exception as exc:
                logger.warning("[mytheresa] Page extraction failed: %s", exc)
            finally:
                await browser.close()

        return None

    async def _extract_price(self, page, url: str) -> tuple[float | None, float]:
        """Try multiple extraction strategies, return (price, confidence)."""

        # Strategy 1: JSON-LD structured data (most reliable, 0.95 confidence)
        try:
            json_ld = await page.evaluate("""
                () => {
                    const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                    for (const s of scripts) {
                        try {
                            const data = JSON.parse(s.textContent);
                            if (data['@type'] === 'Product' && data.offers) {
                                return data.offers.price || data.offers[0]?.price;
                            }
                        } catch(e) {}
                    }
                    return null;
                }
            """)
            if json_ld:
                return float(str(json_ld).replace(",", "")), 0.95
        except Exception:
            pass

        # Strategy 2: data-price attribute (0.90 confidence)
        try:
            price_attr = await page.get_attribute('[data-price]', 'data-price')
            if price_attr:
                return float(price_attr.replace(",", "")), 0.90
        except Exception:
            pass

        # Strategy 3: visible price element (0.75 confidence)
        for selector in self.PRICE_SELECTORS:
            try:
                el = page.locator(selector).first
                text = await el.inner_text(timeout=3000)
                price = _parse_price_text(text)
                if price:
                    return price, 0.75
            except Exception:
                continue

        # Strategy 4: full page text scan (0.50 confidence — last resort)
        try:
            body = await page.inner_text("body")
            price = _parse_price_text(body[:500])  # only scan top of page
            if price:
                return price, 0.50
        except Exception:
            pass

        return None, 0.0

    def build_url(self, slug: str, country: str = "France") -> str:
        """Build a Mytheresa product URL for a given country region."""
        region_map = {
            "France":      "en-fr",
            "Italy":       "en-it",
            "Germany":     "en-de",
            "UK":          "en-gb",
            "USA":         "en-us",
            "Japan":       "en-jp",
            "South Korea": "en-kr",
            "UAE":         "en-ae",
            "Singapore":   "en-sg",
        }
        region = region_map.get(country, "en-fr")
        return f"{self.base_url}/{region}/p-{slug}"


# ── Farfetch Scraper (stub — ready to implement) ──────────────────────────────

class FarfetchScraper(BaseScraper):
    """
    Stub for Farfetch scraper.

    Farfetch uses heavy JavaScript and Cloudflare protection.
    Recommended approach: Playwright with stealth plugin, or use
    their affiliate API if you have partner access.

    To implement:
      1. Install playwright-stealth: pip install playwright-stealth
      2. Use stealth_async(page) before navigation
      3. Target: window.__initialState__.pdp.product.price
    """

    name = "farfetch"
    base_url = "https://www.farfetch.com"

    async def fetch_price(self, url: str, product_id: int, country: str) -> Optional[ScrapedPrice]:
        logger.warning("[farfetch] Scraper not yet implemented. Use Mytheresa instead.")
        return None


# ── Demo Scraper (mock — no browser needed) ───────────────────────────────────

_MOCK_HTML = """
<html><body>
  <div class="product-title">Chanel Classic Flap Medium</div>
  <div class="price-wrapper">
    <span class="price" data-currency="EUR">€10,450</span>
  </div>
  <div class="country-origin">France</div>
</body></html>
"""

class DemoScraper(BaseScraper):
    """Returns mock data — useful for testing without Playwright installed."""

    name = "demo"

    async def fetch_price(self, url: str, product_id: int, country: str) -> Optional[ScrapedPrice]:
        logger.info("[demo] Returning mock price data (no real HTTP request)")
        match = re.search(r"([€£¥₩]?)([\d,]+\.?\d*)", _MOCK_HTML)
        if match:
            price = float(match.group(2).replace(",", ""))
            return ScrapedPrice(
                product_id=product_id,
                country=country,
                currency=COUNTRY_CURRENCIES.get(country, "EUR"),
                price=price,
                source_url="https://demo-fixture",
                confidence=1.0,
            )
        return None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_price_text(text: str) -> float | None:
    """Extract a numeric price from a string like '€10,450' or 'EUR 10450.00'."""
    text = text.strip()
    # Remove currency symbols and codes
    for sym in ["S$", "AED", "€", "£", "¥", "₩", "$", "EUR", "GBP", "JPY", "KRW", "USD", "SGD"]:
        text = text.replace(sym, "")
    # Find first number
    match = re.search(r"([\d]{1,3}(?:[,\.][\d]{3})*(?:[,\.]\d{1,2})?)", text.strip())
    if not match:
        return None
    raw = match.group(1).replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return None


# ── Registry ──────────────────────────────────────────────────────────────────

SCRAPERS: dict[str, BaseScraper] = {
    "mytheresa": MytheresaScraper(),
    "farfetch":  FarfetchScraper(),
    "demo":      DemoScraper(),
}


async def run_scraper(
    scraper_name: str,
    url: str,
    product_id: int,
    country: str,
) -> Optional[ScrapedPrice]:
    scraper = SCRAPERS.get(scraper_name)
    if not scraper:
        raise ValueError(f"Unknown scraper: {scraper_name!r}. Available: {list(SCRAPERS)}")
    return await scraper.run(url, product_id, country)


def get_mytheresa_url(product_id: int, country: str) -> str | None:
    """Build a Mytheresa URL for a product if it has a slug defined."""
    from app.utils.data_store import get_product_by_id
    product = get_product_by_id(product_id)
    if not product or "mytheresa_slug" not in product:
        return None
    scraper = SCRAPERS.get("mytheresa")
    if isinstance(scraper, MytheresaScraper):
        return scraper.build_url(product["mytheresa_slug"], country)
    return None
