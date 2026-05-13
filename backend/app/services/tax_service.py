"""
services/tax_service.py — v3.0

Rule-based VAT and tourist refund config for all 8 supported countries.

Country notes:
  France      – Detaxe ~12% net refund (20% VAT, operator fees deducted)
  Italy       – Similar Detaxe ~13% net (22% VAT)
  Japan       – Full 10% consumption tax refund at point of sale
  Singapore   – GST 9%, no tourist refund for residents
  UK          – VAT 20%, tourist VAT refund scheme ABOLISHED Jan 2021
  USA         – No federal VAT; state sales tax not refundable by tourists
  South Korea – 10% VAT, ~7% net refund after operator fees (Global Blue)
  UAE         – VAT 5%, tourist refund ~4.5% net (Planet / Global Blue)
"""

from typing import TypedDict


class CountryTaxConfig(TypedDict):
    vat_rate: float
    refund_rate: float        # effective tourist refund as % of retail price
    currency: str
    min_spend_local: float    # minimum receipt to qualify (0 = no minimum)
    notes: str


TAX_CONFIG: dict[str, CountryTaxConfig] = {
    "France": {
        "vat_rate":        0.20,
        "refund_rate":     0.12,
        "currency":        "EUR",
        "min_spend_local": 100.01,
        "notes": "Detaxe scheme. Net ~12% after Global Blue / Planet fees. Min €100.01/receipt.",
    },
    "Italy": {
        "vat_rate":        0.22,
        "refund_rate":     0.13,
        "currency":        "EUR",
        "min_spend_local": 154.94,
        "notes": "Tax refund scheme. Net ~13% after fees. Min €154.94/receipt.",
    },
    "Japan": {
        "vat_rate":        0.10,
        "refund_rate":     0.10,
        "currency":        "JPY",
        "min_spend_local": 5000,
        "notes": "Full 10% consumption tax refund at point of sale. Min ¥5,000/store/day.",
    },
    "Singapore": {
        "vat_rate":        0.09,
        "refund_rate":     0.00,
        "currency":        "SGD",
        "min_spend_local": 0,
        "notes": "GST 9%. No tourist refund scheme. Baseline country for comparison.",
    },
    "UK": {
        "vat_rate":        0.20,
        "refund_rate":     0.00,
        "currency":        "GBP",
        "min_spend_local": 0,
        "notes": "VAT 20%. Tourist VAT refund scheme abolished Jan 2021. No refund available.",
    },
    "USA": {
        "vat_rate":        0.00,
        "refund_rate":     0.00,
        "currency":        "USD",
        "min_spend_local": 0,
        "notes": "No federal VAT. Prices shown exclude state sales tax (varies 0–10%). No refund.",
    },
    "South Korea": {
        "vat_rate":        0.10,
        "refund_rate":     0.07,
        "currency":        "KRW",
        "min_spend_local": 30000,
        "notes": "VAT 10%. Tourist refund ~7% net after fees. Min ₩30,000/receipt. Refund at airport.",
    },
    "UAE": {
        "vat_rate":        0.05,
        "refund_rate":     0.045,
        "currency":        "AED",
        "min_spend_local": 250,
        "notes": "VAT 5%. Tourist refund ~4.5% net (Planet scheme). Min AED 250/receipt.",
    },
}

SG_IMPORT_GST_RATE: float = 0.09


def get_tax_config(country: str) -> CountryTaxConfig:
    cfg = TAX_CONFIG.get(country)
    if cfg is None:
        raise ValueError(f"No tax config for country: {country!r}")
    return cfg


def get_all_tax_configs() -> dict[str, CountryTaxConfig]:
    return TAX_CONFIG


def calculate_vat_refund(country: str, local_price: float) -> float:
    cfg = get_tax_config(country)
    if local_price < cfg["min_spend_local"]:
        return 0.0
    return round(local_price * cfg["refund_rate"], 2)
