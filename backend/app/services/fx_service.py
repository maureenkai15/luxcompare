"""
services/fx_service.py — v3.0

Fetches live EUR/JPY/GBP/USD/KRW/AED → SGD exchange rates.
Tries three free providers in order until one succeeds.

Fallback: hardcoded mid-2025 approximate rates.
Cache TTL: 15 minutes (FX_CACHE_TTL_SECONDS env var).
"""

import time
import logging
import os
from typing import Dict, List, Tuple

import httpx

logger = logging.getLogger(__name__)

_API_PROVIDERS: List[Tuple[str, str]] = [
    ("https://open.er-api.com/v6/latest/SGD",         "rates"),
    ("https://api.exchangerate-api.com/v4/latest/SGD", "rates"),
    ("https://api.frankfurter.app/latest?from=SGD&to=EUR,JPY,GBP,USD,KRW,AED", "rates"),
]

_CACHE_TTL       = int(os.getenv("FX_CACHE_TTL_SECONDS", "900"))
_REQUEST_TIMEOUT = 8.0

_FALLBACK_RATES: Dict[str, float] = {
    "EUR": 1.46,
    "JPY": 0.0092,
    "GBP": 1.71,
    "USD": 1.35,
    "KRW": 0.00099,
    "AED": 0.368,
    "SGD": 1.00,
}

_cache: Dict = {
    "rates":      {},
    "fetched_at": 0.0,
    "source":     "none",
    "live_ok":    False,
}


def _is_stale() -> bool:
    return (time.time() - _cache["fetched_at"]) > _CACHE_TTL


def _invert_rates(raw: Dict[str, float]) -> Dict[str, float]:
    result: Dict[str, float] = {"SGD": 1.0}
    for currency, sgd_per_unit in raw.items():
        if sgd_per_unit and sgd_per_unit != 0:
            result[currency] = round(1.0 / sgd_per_unit, 6)
    return result


async def _fetch_from_api(url: str) -> Dict[str, float] | None:
    try:
        async with httpx.AsyncClient(timeout=_REQUEST_TIMEOUT) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            raw_rates = data.get("rates") or data.get("conversion_rates")
            if not raw_rates:
                return None
            return _invert_rates(raw_rates)
    except Exception as exc:
        logger.warning("FX fetch failed from %s: %s", url, exc)
        return None


async def refresh_rates() -> None:
    for url, _ in _API_PROVIDERS:
        rates = await _fetch_from_api(url)
        if rates:
            # Ensure all currencies have a rate (Frankfurter may omit some)
            for cur, fallback in _FALLBACK_RATES.items():
                if cur not in rates:
                    rates[cur] = fallback
            _cache["rates"]      = rates
            _cache["fetched_at"] = time.time()
            _cache["source"]     = "live"
            _cache["live_ok"]    = True
            logger.info("FX rates refreshed. EUR→SGD=%.4f KRW→SGD=%.6f AED→SGD=%.4f",
                        rates.get("EUR", 0), rates.get("KRW", 0), rates.get("AED", 0))
            return

    _cache["rates"]      = _FALLBACK_RATES.copy()
    _cache["fetched_at"] = time.time()
    _cache["source"]     = "fallback"
    _cache["live_ok"]    = False
    logger.warning("All FX providers unreachable — using hardcoded fallback rates.")


async def get_rates() -> Dict[str, float]:
    if _is_stale() or not _cache["rates"]:
        await refresh_rates()
    return _cache["rates"]


async def get_rate(currency: str) -> float:
    rates = await get_rates()
    rate = rates.get(currency.upper())
    if rate is None:
        fallback = _FALLBACK_RATES.get(currency.upper())
        if fallback is None:
            raise ValueError(f"Unknown currency: {currency}")
        return fallback
    return rate


def get_cache_meta() -> Dict:
    return {
        "fetched_at":     _cache["fetched_at"],
        "fetched_at_iso": _ts_to_iso(_cache["fetched_at"]),
        "source":         _cache["source"],
        "live_ok":        _cache["live_ok"],
        "ttl_seconds":    _CACHE_TTL,
        "age_seconds":    round(time.time() - _cache["fetched_at"], 1),
        "currencies":     list(_cache["rates"].keys()),
    }


def _ts_to_iso(ts: float) -> str:
    import datetime
    if ts == 0:
        return "never"
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
