# LuxCompare AI — v2.0

> **Global Luxury Price Intelligence** — Compare Chanel, Louis Vuitton, Dior & Hermès prices
> across France, Italy, Japan and Singapore, with **live FX rates**, VAT refunds, and Singapore import GST.

---

## What's New in v2.0

| Feature | v1 (MVP) | v2 (Upgraded) |
|---|---|---|
| Exchange rates | Hardcoded static | **Live API** — 3 providers, 15-min cache, fallback |
| Price data | Single hardcoded dict | **3-tier provider chain** (scraped → CSV → static) |
| VAT rules | Hardcoded numbers | **Config-driven** with min-spend thresholds per country |
| Scraping | None | **Extensible framework** — BaseScraper + DemoScraper |
| Frontend | Basic compare | **FX status indicator** + price source badge |
| Backend | Single service file | **Modular** fx / tax / price / scraper services |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Next.js Frontend                    │
│  SearchBar → ComparisonTable → RecommendationCard       │
│  FxStatus (live/fallback badge + last-updated time)     │
│  PriceSourceBadge (scraped / csv / static)              │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP (localhost:8000)
┌────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend                       │
│                                                         │
│  Routes: /search  /compare  /calculate  /fx  /admin     │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  fx_service │  │ price_service│  │  tax_service │   │
│  │ • 3 FX APIs │  │ Provider     │  │ VAT configs  │   │
│  │ • 15m cache │  │ chain:       │  │ Min-spend    │   │
│  │ • fallback  │  │  1. Scraped  │  │ thresholds   │   │
│  └─────────────┘  │  2. CSV      │  └──────────────┘   │
│                   │  3. Static   │                      │
│  ┌─────────────┐  └──────────────┘                     │
│  │scraper_svc  │                                        │
│  │ BaseScraper │                                        │
│  │ DemoScraper │                                        │
│  │ (+ future)  │                                        │
│  └─────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start (2 commands)

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1 — Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # optional — defaults work out of the box
uvicorn main:app --reload --port 8000
```

App starts, FX rates warm up automatically.

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### 2 — Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local  # optional — defaults to localhost:8000
npm run dev
```

- App: http://localhost:3000

---

## Project Structure

```
luxcompare/
├── backend/
│   ├── main.py                      # FastAPI app + startup FX warm-up
│   ├── requirements.txt
│   ├── .env.example
│   ├── schema.sql                   # PostgreSQL schema + full seed data
│   ├── data/
│   │   └── prices_override.csv      # Optional CSV price overrides (empty)
│   └── app/
│       ├── routes/
│       │   ├── search.py            # GET  /search?q=
│       │   ├── compare.py           # GET  /compare/{product_id}
│       │   ├── calculate.py         # POST /calculate
│       │   ├── fx.py                # GET  /fx  ·  POST /fx/refresh
│       │   └── admin.py             # /admin/tax-config, reload-csv, scrape
│       ├── services/
│       │   ├── fx_service.py        # Live FX rates, cache, fallback
│       │   ├── price_service.py     # 3-tier provider chain abstraction
│       │   ├── price_calculator.py  # Core formula (async, live rates)
│       │   ├── tax_service.py       # Country VAT config + min-spend rules
│       │   ├── search_service.py    # Fuzzy substring product search
│       │   └── scraper_service.py   # BaseScraper interface + DemoScraper
│       └── utils/
│           └── data_store.py        # Static dataset — 15 products, 4 countries
│
└── frontend/
    ├── .env.local.example
    └── src/
        ├── app/
        │   ├── layout.tsx
        │   ├── page.tsx             # Main page (search + results)
        │   └── globals.css
        ├── components/
        │   ├── Header.tsx
        │   ├── SearchBar.tsx        # Debounced search + brand chips
        │   ├── ComparisonTable.tsx  # Country table with savings column
        │   ├── RecommendationCard.tsx
        │   ├── PriceBreakdown.tsx   # Expandable per-country breakdown
        │   ├── FxStatus.tsx         # Live/fallback badge + timestamp
        │   └── PriceSourceBadge.tsx # Scraped / CSV / static indicator
        └── lib/
            ├── api.ts               # Typed API client
            └── format.ts            # SGD + local currency formatters
```

---

## Calculation Formula

```
final_price_sgd = (retail_price_local − vat_refund) × exchange_rate_to_sgd + import_gst
```

- `vat_refund = retail_price_local × refund_rate`  (0 if price is below min spend)
- `import_gst = price_after_refund_sgd × 0.09`  (Singapore GST on overseas items only)

### VAT Config (`tax_service.py`)

| Country | VAT Rate | Tourist Refund | Min Spend |
|---|---|---|---|
| France | 20% | ~12% of retail | €100.01 |
| Italy | 22% | ~13% of retail | €154.94 |
| Japan | 10% | 10% (full) | ¥5,000 |
| Singapore | 9% | 0% | — |

---

## FX Rate System

**Provider waterfall** — first success wins:

1. `open.er-api.com` — no API key, generous free tier
2. `api.exchangerate-api.com` — no-key legacy endpoint
3. `api.frankfurter.app` — ECB data, very reliable

**Cache:** 15-minute in-memory TTL (set `FX_CACHE_TTL_SECONDS` in `.env`).  
**Fallback:** Hardcoded mid-2025 approximate rates if all three providers fail.  
**Frontend:** FxStatus shows `LIVE FX` (green) or `FALLBACK FX` (amber) + last-updated timestamp.

---

## Price Provider Chain

```
ScrapedPriceProvider  →  results injected by POST /admin/scrape
        ↓ (empty at startup)
CsvPriceProvider      →  reads data/prices_override.csv
        ↓ (file absent or no matching rows)
StaticPriceProvider   →  always available, hardcoded 15-product dataset
```

Every `/compare` response includes `price_source: "scraped" | "csv" | "static"`.

---

## API Reference

### `GET /search?q={query}`
Search by brand or product name.

### `GET /compare/{product_id}`
Full VAT-adjusted, live-FX comparison for a product.
Returns `comparisons[]`, `recommendation`, `cheapest_country`, `price_source`, `fx_meta`.

### `POST /calculate`
Ad-hoc calculation for any price/country not in the catalogue.
```json
{ "country": "France", "currency": "EUR", "local_price": 10300 }
```

### `GET /fx`
Current exchange rates + cache metadata (source, age, TTL).

### `POST /fx/refresh`
Force-refresh FX cache from live API, ignoring TTL.

### `GET /admin/tax-config`
View all country VAT rules.

### `POST /admin/reload-csv`
Hot-reload `prices_override.csv` without restarting the server.

### `POST /admin/scrape`
Trigger a scraper and inject results into ScrapedPriceProvider.
```json
{ "scraper": "demo", "url": "https://...", "product_id": 1, "country": "France" }
```

### `GET /admin/scrapers`
List registered scraper names.

---

## Injecting CSV Price Overrides

Edit `backend/data/prices_override.csv`:

```csv
product_id,country,currency,price
1,France,EUR,10850
7,Italy,EUR,5750
```

Then `POST /admin/reload-csv` — no server restart needed.  
The response badge will show `CSV override` for those products.

---

## Adding a Real Scraper

```python
# In scraper_service.py

class MytheresaScraper(BaseScraper):
    name = "mytheresa"
    base_url = "https://www.mytheresa.com"

    async def fetch_html(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            return resp.text

    def parse(self, html: str, product_id: int, country: str) -> ScrapedPrice | None:
        soup = BeautifulSoup(html, "html.parser")
        price_tag = soup.select_one(".price-tag")          # real selector here
        if not price_tag: return None
        price = float(price_tag.text.replace(",", "").strip("€"))
        return ScrapedPrice(product_id=product_id, country=country,
                            currency="EUR", price=price,
                            source_url=self.base_url, confidence=0.9)

# Register it
SCRAPERS = {
    "demo": DemoScraper(),
    "mytheresa": MytheresaScraper(),
}
```

> Always check `robots.txt` and Terms of Service before scraping.

---

## Environment Variables

### Backend (`.env`)

| Variable | Default | Description |
|---|---|---|
| `FX_CACHE_TTL_SECONDS` | `900` | FX cache TTL in seconds |
| `PRICE_CSV_PATH` | `data/prices_override.csv` | Path to CSV overrides |
| `DATABASE_URL` | — | PostgreSQL URL (optional) |

### Frontend (`.env.local`)

| Variable | Default | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API base URL |

---

## Example API Response — `/compare/1`

```json
{
  "product_id": 1,
  "brand": "Chanel",
  "product_name": "Classic Flap Medium",
  "cheapest_country": "Italy",
  "cheapest_final_sgd": 14261,
  "recommendation": "Italy is currently the cheapest country to purchase this item, with an estimated all-in cost of S$14,261 — saving you approximately S$1,239 compared to buying in Singapore.",
  "price_source": "static",
  "fx_meta": {
    "source": "live",
    "live_ok": true,
    "fetched_at": "2025-06-15T08:32:00Z",
    "age_seconds": 43.2
  },
  "comparisons": [
    {
      "country": "Italy",
      "currency": "EUR",
      "local_price": 10300,
      "vat_refund_rate": 0.13,
      "vat_refund_local": 1339.0,
      "price_after_refund_local": 8961.0,
      "exchange_rate_to_sgd": 1.46,
      "price_after_refund_sgd": 13083.06,
      "import_gst_sgd": 1177.48,
      "final_price_sgd": 14260.54,
      "savings_vs_sg": 1239.46
    }
  ]
}
```

---

## Roadmap

- [ ] Auto-refresh FX in frontend (polling or WebSocket)
- [ ] Real scraper implementations (Farfetch, Mytheresa, Net-a-Porter)
- [ ] PostgreSQL backend (swap `data_store.py` for DB queries)
- [ ] Price history charts per product
- [ ] More countries (UK, USA, South Korea)
- [ ] AI chatbot — "cheapest Hermès bag in Europe?"

---

## Disclaimer

Prices are indicative only. VAT refund rates, exchange rates, and duties may vary.  
Always verify with the retailer and Singapore Customs (customs.gov.sg) before purchasing.  
Not financial advice.

---

*LuxCompare AI v2.0 — Portfolio project*
