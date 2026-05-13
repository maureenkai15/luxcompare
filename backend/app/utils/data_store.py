"""
LuxCompare AI — Static dataset v3.0

Brands:    Chanel, Louis Vuitton, Dior, Hermès, Bottega Veneta, Celine
Countries: Singapore, France, Italy, Japan, UK, USA, South Korea, UAE
Prices:    manually researched from brand websites (mid-2025)
"""
from typing import Dict, List

# ── Fallback exchange rates (live rates fetched by fx_service) ────────────────
EXCHANGE_RATES: Dict[str, float] = {
    "EUR": 1.46,
    "JPY": 0.0092,
    "SGD": 1.00,
    "USD": 1.35,
    "GBP": 1.71,
    "KRW": 0.00099,
    "AED": 0.368,
}

# ── VAT / refund rules (kept for legacy compatibility) ────────────────────────
VAT_RULES: Dict[str, Dict] = {
    "France":      {"vat_rate": 0.20, "refund_rate": 0.12, "currency": "EUR"},
    "Italy":       {"vat_rate": 0.22, "refund_rate": 0.13, "currency": "EUR"},
    "Japan":       {"vat_rate": 0.10, "refund_rate": 0.10, "currency": "JPY"},
    "Singapore":   {"vat_rate": 0.09, "refund_rate": 0.00, "currency": "SGD"},
    "UK":          {"vat_rate": 0.20, "refund_rate": 0.00, "currency": "GBP"},
    "USA":         {"vat_rate": 0.00, "refund_rate": 0.00, "currency": "USD"},
    "South Korea": {"vat_rate": 0.10, "refund_rate": 0.07, "currency": "KRW"},
    "UAE":         {"vat_rate": 0.05, "refund_rate": 0.045, "currency": "AED"},
}

SG_IMPORT_GST_RATE = 0.09

# ── Products ──────────────────────────────────────────────────────────────────
PRODUCTS: List[Dict] = [

    # ── CHANEL ────────────────────────────────────────────────
    {
        "id": 1, "brand": "Chanel", "category": "Handbag",
        "product_name": "Classic Flap Medium",
        "description": "Iconic quilted lambskin or caviar flap bag with interlocking CC clasp",
        "mytheresa_slug": "chanel-classic-flap-medium",
        "prices": {
            "France":      {"currency": "EUR", "price": 10300},
            "Italy":       {"currency": "EUR", "price": 10300},
            "Japan":       {"currency": "JPY", "price": 1694000},
            "Singapore":   {"currency": "SGD", "price": 15500},
            "UK":          {"currency": "GBP", "price": 8790},
            "USA":         {"currency": "USD", "price": 10800},
            "South Korea": {"currency": "KRW", "price": 14560000},
            "UAE":         {"currency": "AED", "price": 39500},
        },
    },
    {
        "id": 2, "brand": "Chanel", "category": "Handbag",
        "product_name": "Classic Flap Small",
        "description": "Compact quilted lambskin flap bag, perfect for evenings",
        "mytheresa_slug": "chanel-classic-flap-small",
        "prices": {
            "France":      {"currency": "EUR", "price": 8900},
            "Italy":       {"currency": "EUR", "price": 8900},
            "Japan":       {"currency": "JPY", "price": 1463000},
            "Singapore":   {"currency": "SGD", "price": 13400},
            "UK":          {"currency": "GBP", "price": 7590},
            "USA":         {"currency": "USD", "price": 9300},
            "South Korea": {"currency": "KRW", "price": 12560000},
            "UAE":         {"currency": "AED", "price": 34100},
        },
    },
    {
        "id": 3, "brand": "Chanel", "category": "Handbag",
        "product_name": "Boy Bag Medium",
        "description": "Structured leather bag with ruthenium chain and CC clasp",
        "mytheresa_slug": "chanel-boy-bag-medium",
        "prices": {
            "France":      {"currency": "EUR", "price": 9400},
            "Italy":       {"currency": "EUR", "price": 9400},
            "Japan":       {"currency": "JPY", "price": 1540000},
            "Singapore":   {"currency": "SGD", "price": 14200},
            "UK":          {"currency": "GBP", "price": 8010},
            "USA":         {"currency": "USD", "price": 9850},
            "South Korea": {"currency": "KRW", "price": 13300000},
            "UAE":         {"currency": "AED", "price": 36000},
        },
    },
    {
        "id": 4, "brand": "Chanel", "category": "Handbag",
        "product_name": "Gabrielle Hobo Bag",
        "description": "Casual yet luxurious hobo with multi-chain strap system",
        "mytheresa_slug": "chanel-gabrielle-hobo",
        "prices": {
            "France":      {"currency": "EUR", "price": 4550},
            "Italy":       {"currency": "EUR", "price": 4550},
            "Japan":       {"currency": "JPY", "price": 745000},
            "Singapore":   {"currency": "SGD", "price": 6900},
            "UK":          {"currency": "GBP", "price": 3890},
            "USA":         {"currency": "USD", "price": 4750},
            "South Korea": {"currency": "KRW", "price": 6440000},
            "UAE":         {"currency": "AED", "price": 17500},
        },
    },
    {
        "id": 5, "brand": "Chanel", "category": "Handbag",
        "product_name": "19 Bag Large",
        "description": "Soft quilted leather bag with mixed metal chain, Karl Lagerfeld's last design",
        "mytheresa_slug": "chanel-19-bag-large",
        "prices": {
            "France":      {"currency": "EUR", "price": 6000},
            "Italy":       {"currency": "EUR", "price": 6000},
            "Japan":       {"currency": "JPY", "price": 985000},
            "Singapore":   {"currency": "SGD", "price": 9100},
            "UK":          {"currency": "GBP", "price": 5120},
            "USA":         {"currency": "USD", "price": 6250},
            "South Korea": {"currency": "KRW", "price": 8490000},
            "UAE":         {"currency": "AED", "price": 23000},
        },
    },
    {
        "id": 6, "brand": "Chanel", "category": "Handbag",
        "product_name": "Mini Rectangular Flap",
        "description": "Mini quilted flap with top handle and chain strap — highly sought after",
        "mytheresa_slug": "chanel-mini-rectangular-flap",
        "prices": {
            "France":      {"currency": "EUR", "price": 4400},
            "Italy":       {"currency": "EUR", "price": 4400},
            "Japan":       {"currency": "JPY", "price": 722000},
            "Singapore":   {"currency": "SGD", "price": 6700},
            "UK":          {"currency": "GBP", "price": 3760},
            "USA":         {"currency": "USD", "price": 4600},
            "South Korea": {"currency": "KRW", "price": 6200000},
            "UAE":         {"currency": "AED", "price": 16900},
        },
    },

    # ── LOUIS VUITTON ─────────────────────────────────────────
    {
        "id": 7, "brand": "Louis Vuitton", "category": "Handbag",
        "product_name": "Neverfull MM",
        "description": "Spacious Monogram canvas tote — the world's best-selling luxury bag",
        "mytheresa_slug": "louis-vuitton-neverfull-mm",
        "prices": {
            "France":      {"currency": "EUR", "price": 1630},
            "Italy":       {"currency": "EUR", "price": 1630},
            "Japan":       {"currency": "JPY", "price": 269500},
            "Singapore":   {"currency": "SGD", "price": 2630},
            "UK":          {"currency": "GBP", "price": 1390},
            "USA":         {"currency": "USD", "price": 1700},
            "South Korea": {"currency": "KRW", "price": 2310000},
            "UAE":         {"currency": "AED", "price": 6250},
        },
    },
    {
        "id": 8, "brand": "Louis Vuitton", "category": "Handbag",
        "product_name": "Speedy Bandouliere 25",
        "description": "Classic doctor-bag silhouette in Monogram canvas with adjustable strap",
        "mytheresa_slug": "louis-vuitton-speedy-25",
        "prices": {
            "France":      {"currency": "EUR", "price": 1520},
            "Italy":       {"currency": "EUR", "price": 1520},
            "Japan":       {"currency": "JPY", "price": 251000},
            "Singapore":   {"currency": "SGD", "price": 2450},
            "UK":          {"currency": "GBP", "price": 1300},
            "USA":         {"currency": "USD", "price": 1590},
            "South Korea": {"currency": "KRW", "price": 2150000},
            "UAE":         {"currency": "AED", "price": 5830},
        },
    },
    {
        "id": 9, "brand": "Louis Vuitton", "category": "Handbag",
        "product_name": "Capucines MM",
        "description": "Refined structured tote in supple Taurillon leather — top of the LV range",
        "mytheresa_slug": "louis-vuitton-capucines-mm",
        "prices": {
            "France":      {"currency": "EUR", "price": 5550},
            "Italy":       {"currency": "EUR", "price": 5550},
            "Japan":       {"currency": "JPY", "price": 912000},
            "Singapore":   {"currency": "SGD", "price": 8500},
            "UK":          {"currency": "GBP", "price": 4740},
            "USA":         {"currency": "USD", "price": 5800},
            "South Korea": {"currency": "KRW", "price": 7860000},
            "UAE":         {"currency": "AED", "price": 21300},
        },
    },
    {
        "id": 10, "brand": "Louis Vuitton", "category": "Handbag",
        "product_name": "Twist MM",
        "description": "Structured flap with iconic LV twist-lock in Epi or Monogram leather",
        "mytheresa_slug": "louis-vuitton-twist-mm",
        "prices": {
            "France":      {"currency": "EUR", "price": 4800},
            "Italy":       {"currency": "EUR", "price": 4800},
            "Japan":       {"currency": "JPY", "price": 786000},
            "Singapore":   {"currency": "SGD", "price": 7300},
            "UK":          {"currency": "GBP", "price": 4100},
            "USA":         {"currency": "USD", "price": 5000},
            "South Korea": {"currency": "KRW", "price": 6800000},
            "UAE":         {"currency": "AED", "price": 18400},
        },
    },
    {
        "id": 11, "brand": "Louis Vuitton", "category": "Handbag",
        "product_name": "OnTheGo GM",
        "description": "Oversized reversible tote in Monogram and Monogram reverse canvas",
        "mytheresa_slug": "louis-vuitton-onthego-gm",
        "prices": {
            "France":      {"currency": "EUR", "price": 3400},
            "Italy":       {"currency": "EUR", "price": 3400},
            "Japan":       {"currency": "JPY", "price": 559000},
            "Singapore":   {"currency": "SGD", "price": 5200},
            "UK":          {"currency": "GBP", "price": 2910},
            "USA":         {"currency": "USD", "price": 3550},
            "South Korea": {"currency": "KRW", "price": 4820000},
            "UAE":         {"currency": "AED", "price": 13050},
        },
    },
    {
        "id": 12, "brand": "Louis Vuitton", "category": "Handbag",
        "product_name": "Dauphine MM",
        "description": "Monogram flap bag with LV clasp — elegant and versatile",
        "mytheresa_slug": "louis-vuitton-dauphine-mm",
        "prices": {
            "France":      {"currency": "EUR", "price": 3450},
            "Italy":       {"currency": "EUR", "price": 3450},
            "Japan":       {"currency": "JPY", "price": 567000},
            "Singapore":   {"currency": "SGD", "price": 5300},
            "UK":          {"currency": "GBP", "price": 2950},
            "USA":         {"currency": "USD", "price": 3600},
            "South Korea": {"currency": "KRW", "price": 4890000},
            "UAE":         {"currency": "AED", "price": 13230},
        },
    },

    # ── DIOR ──────────────────────────────────────────────────
    {
        "id": 13, "brand": "Dior", "category": "Handbag",
        "product_name": "Lady Dior Medium",
        "description": "Structured cannage-stitched lambskin bag with D.I.O.R charms",
        "mytheresa_slug": "dior-lady-dior-medium",
        "prices": {
            "France":      {"currency": "EUR", "price": 5600},
            "Italy":       {"currency": "EUR", "price": 5600},
            "Japan":       {"currency": "JPY", "price": 913000},
            "Singapore":   {"currency": "SGD", "price": 8600},
            "UK":          {"currency": "GBP", "price": 4790},
            "USA":         {"currency": "USD", "price": 5850},
            "South Korea": {"currency": "KRW", "price": 7940000},
            "UAE":         {"currency": "AED", "price": 21500},
        },
    },
    {
        "id": 14, "brand": "Dior", "category": "Handbag",
        "product_name": "Lady Dior Small",
        "description": "Compact cannage-stitched lambskin bag — Princess Diana's iconic choice",
        "mytheresa_slug": "dior-lady-dior-small",
        "prices": {
            "France":      {"currency": "EUR", "price": 4800},
            "Italy":       {"currency": "EUR", "price": 4800},
            "Japan":       {"currency": "JPY", "price": 783000},
            "Singapore":   {"currency": "SGD", "price": 7400},
            "UK":          {"currency": "GBP", "price": 4100},
            "USA":         {"currency": "USD", "price": 5000},
            "South Korea": {"currency": "KRW", "price": 6810000},
            "UAE":         {"currency": "AED", "price": 18400},
        },
    },
    {
        "id": 15, "brand": "Dior", "category": "Handbag",
        "product_name": "Book Tote Large",
        "description": "Oversized embroidered canvas tote — a collector's statement piece",
        "mytheresa_slug": "dior-book-tote-large",
        "prices": {
            "France":      {"currency": "EUR", "price": 3100},
            "Italy":       {"currency": "EUR", "price": 3100},
            "Japan":       {"currency": "JPY", "price": 506000},
            "Singapore":   {"currency": "SGD", "price": 4700},
            "UK":          {"currency": "GBP", "price": 2650},
            "USA":         {"currency": "USD", "price": 3200},
            "South Korea": {"currency": "KRW", "price": 4400000},
            "UAE":         {"currency": "AED", "price": 11900},
        },
    },
    {
        "id": 16, "brand": "Dior", "category": "Handbag",
        "product_name": "Saddle Bag",
        "description": "Curved saddle silhouette in Dior Oblique canvas — a fashion icon",
        "mytheresa_slug": "dior-saddle-bag",
        "prices": {
            "France":      {"currency": "EUR", "price": 3600},
            "Italy":       {"currency": "EUR", "price": 3600},
            "Japan":       {"currency": "JPY", "price": 588000},
            "Singapore":   {"currency": "SGD", "price": 5500},
            "UK":          {"currency": "GBP", "price": 3080},
            "USA":         {"currency": "USD", "price": 3750},
            "South Korea": {"currency": "KRW", "price": 5100000},
            "UAE":         {"currency": "AED", "price": 13800},
        },
    },
    {
        "id": 17, "brand": "Dior", "category": "Handbag",
        "product_name": "Miss Dior Mini Bag",
        "description": "Petite quilted lambskin crossbody with CD signature buckle",
        "mytheresa_slug": "dior-miss-dior-mini",
        "prices": {
            "France":      {"currency": "EUR", "price": 3200},
            "Italy":       {"currency": "EUR", "price": 3200},
            "Japan":       {"currency": "JPY", "price": 522000},
            "Singapore":   {"currency": "SGD", "price": 4900},
            "UK":          {"currency": "GBP", "price": 2740},
            "USA":         {"currency": "USD", "price": 3350},
            "South Korea": {"currency": "KRW", "price": 4540000},
            "UAE":         {"currency": "AED", "price": 12300},
        },
    },
    {
        "id": 18, "brand": "Dior", "category": "Handbag",
        "product_name": "30 Montaigne Box Bag",
        "description": "Structured box bag with signature CD clasp — named after Dior's Paris HQ",
        "mytheresa_slug": "dior-30-montaigne-box",
        "prices": {
            "France":      {"currency": "EUR", "price": 4150},
            "Italy":       {"currency": "EUR", "price": 4150},
            "Japan":       {"currency": "JPY", "price": 678000},
            "Singapore":   {"currency": "SGD", "price": 6350},
            "UK":          {"currency": "GBP", "price": 3550},
            "USA":         {"currency": "USD", "price": 4300},
            "South Korea": {"currency": "KRW", "price": 5890000},
            "UAE":         {"currency": "AED", "price": 15900},
        },
    },

    # ── HERMES ────────────────────────────────────────────────
    {
        "id": 19, "brand": "Hermes", "category": "Handbag",
        "product_name": "Birkin 25",
        "description": "Handstitched Togo leather tote — the world's most coveted luxury bag",
        "mytheresa_slug": "hermes-birkin-25",
        "prices": {
            "France":      {"currency": "EUR", "price": 9600},
            "Italy":       {"currency": "EUR", "price": 9800},
            "Japan":       {"currency": "JPY", "price": 1540000},
            "Singapore":   {"currency": "SGD", "price": 16000},
            "UK":          {"currency": "GBP", "price": 8200},
            "USA":         {"currency": "USD", "price": 10000},
            "South Korea": {"currency": "KRW", "price": 13600000},
            "UAE":         {"currency": "AED", "price": 36800},
        },
    },
    {
        "id": 20, "brand": "Hermes", "category": "Handbag",
        "product_name": "Birkin 30",
        "description": "The classic Birkin in Togo or Clemence leather — the definitive investment piece",
        "mytheresa_slug": "hermes-birkin-30",
        "prices": {
            "France":      {"currency": "EUR", "price": 10400},
            "Italy":       {"currency": "EUR", "price": 10600},
            "Japan":       {"currency": "JPY", "price": 1672000},
            "Singapore":   {"currency": "SGD", "price": 17500},
            "UK":          {"currency": "GBP", "price": 8900},
            "USA":         {"currency": "USD", "price": 10900},
            "South Korea": {"currency": "KRW", "price": 14800000},
            "UAE":         {"currency": "AED", "price": 39900},
        },
    },
    {
        "id": 21, "brand": "Hermes", "category": "Handbag",
        "product_name": "Kelly 28",
        "description": "Structured trapezoid bag with iconic turn-lock — Grace Kelly's signature",
        "mytheresa_slug": "hermes-kelly-28",
        "prices": {
            "France":      {"currency": "EUR", "price": 10200},
            "Italy":       {"currency": "EUR", "price": 10400},
            "Japan":       {"currency": "JPY", "price": 1650000},
            "Singapore":   {"currency": "SGD", "price": 17000},
            "UK":          {"currency": "GBP", "price": 8720},
            "USA":         {"currency": "USD", "price": 10650},
            "South Korea": {"currency": "KRW", "price": 14450000},
            "UAE":         {"currency": "AED", "price": 39100},
        },
    },
    {
        "id": 22, "brand": "Hermes", "category": "Handbag",
        "product_name": "Kelly 25",
        "description": "Compact Kelly in Epsom leather — the most wearable Kelly size",
        "mytheresa_slug": "hermes-kelly-25",
        "prices": {
            "France":      {"currency": "EUR", "price": 9500},
            "Italy":       {"currency": "EUR", "price": 9700},
            "Japan":       {"currency": "JPY", "price": 1540000},
            "Singapore":   {"currency": "SGD", "price": 15900},
            "UK":          {"currency": "GBP", "price": 8120},
            "USA":         {"currency": "USD", "price": 9900},
            "South Korea": {"currency": "KRW", "price": 13500000},
            "UAE":         {"currency": "AED", "price": 36400},
        },
    },
    {
        "id": 23, "brand": "Hermes", "category": "Handbag",
        "product_name": "Constance 24",
        "description": "Sleek shoulder bag with signature H-buckle clasp — understated elegance",
        "mytheresa_slug": "hermes-constance-24",
        "prices": {
            "France":      {"currency": "EUR", "price": 8700},
            "Italy":       {"currency": "EUR", "price": 8900},
            "Japan":       {"currency": "JPY", "price": 1400000},
            "Singapore":   {"currency": "SGD", "price": 14500},
            "UK":          {"currency": "GBP", "price": 7440},
            "USA":         {"currency": "USD", "price": 9100},
            "South Korea": {"currency": "KRW", "price": 12350000},
            "UAE":         {"currency": "AED", "price": 33400},
        },
    },
    {
        "id": 24, "brand": "Hermes", "category": "Handbag",
        "product_name": "Evelyne III 29",
        "description": "Perforated H canvas crossbody — the most accessible Hermes bag",
        "mytheresa_slug": "hermes-evelyne-29",
        "prices": {
            "France":      {"currency": "EUR", "price": 2950},
            "Italy":       {"currency": "EUR", "price": 3000},
            "Japan":       {"currency": "JPY", "price": 481000},
            "Singapore":   {"currency": "SGD", "price": 5050},
            "UK":          {"currency": "GBP", "price": 2530},
            "USA":         {"currency": "USD", "price": 3100},
            "South Korea": {"currency": "KRW", "price": 4200000},
            "UAE":         {"currency": "AED", "price": 11320},
        },
    },

    # ── BOTTEGA VENETA ────────────────────────────────────────
    {
        "id": 25, "brand": "Bottega Veneta", "category": "Handbag",
        "product_name": "Jodie Bag",
        "description": "Soft intrecciato woven leather hobo — Bottega's signature weave",
        "mytheresa_slug": "bottega-veneta-jodie",
        "prices": {
            "France":      {"currency": "EUR", "price": 3200},
            "Italy":       {"currency": "EUR", "price": 3200},
            "Japan":       {"currency": "JPY", "price": 524000},
            "Singapore":   {"currency": "SGD", "price": 4950},
            "UK":          {"currency": "GBP", "price": 2740},
            "USA":         {"currency": "USD", "price": 3350},
            "South Korea": {"currency": "KRW", "price": 4560000},
            "UAE":         {"currency": "AED", "price": 12300},
        },
    },
    {
        "id": 26, "brand": "Bottega Veneta", "category": "Handbag",
        "product_name": "Cassette Bag",
        "description": "Padded intrecciato crossbody — Daniel Lee's breakthrough design",
        "mytheresa_slug": "bottega-veneta-cassette",
        "prices": {
            "France":      {"currency": "EUR", "price": 3100},
            "Italy":       {"currency": "EUR", "price": 3100},
            "Japan":       {"currency": "JPY", "price": 508000},
            "Singapore":   {"currency": "SGD", "price": 4800},
            "UK":          {"currency": "GBP", "price": 2650},
            "USA":         {"currency": "USD", "price": 3250},
            "South Korea": {"currency": "KRW", "price": 4400000},
            "UAE":         {"currency": "AED", "price": 11900},
        },
    },
    {
        "id": 27, "brand": "Bottega Veneta", "category": "Handbag",
        "product_name": "Arco 33 Tote",
        "description": "Mini intrecciato tote with rolled handles — elegant everyday bag",
        "mytheresa_slug": "bottega-veneta-arco-33",
        "prices": {
            "France":      {"currency": "EUR", "price": 2950},
            "Italy":       {"currency": "EUR", "price": 2950},
            "Japan":       {"currency": "JPY", "price": 483000},
            "Singapore":   {"currency": "SGD", "price": 4550},
            "UK":          {"currency": "GBP", "price": 2520},
            "USA":         {"currency": "USD", "price": 3080},
            "South Korea": {"currency": "KRW", "price": 4180000},
            "UAE":         {"currency": "AED", "price": 11320},
        },
    },
    {
        "id": 28, "brand": "Bottega Veneta", "category": "Handbag",
        "product_name": "Sardine Bag",
        "description": "Structured top-handle in Maxiweave intrecciato — a modern icon",
        "mytheresa_slug": "bottega-veneta-sardine",
        "prices": {
            "France":      {"currency": "EUR", "price": 4200},
            "Italy":       {"currency": "EUR", "price": 4200},
            "Japan":       {"currency": "JPY", "price": 688000},
            "Singapore":   {"currency": "SGD", "price": 6500},
            "UK":          {"currency": "GBP", "price": 3590},
            "USA":         {"currency": "USD", "price": 4400},
            "South Korea": {"currency": "KRW", "price": 5960000},
            "UAE":         {"currency": "AED", "price": 16100},
        },
    },
    {
        "id": 29, "brand": "Bottega Veneta", "category": "Handbag",
        "product_name": "Andiamo Large Tote",
        "description": "Sleek structured tote in intrecciato leather with top handles",
        "mytheresa_slug": "bottega-veneta-andiamo-large",
        "prices": {
            "France":      {"currency": "EUR", "price": 3800},
            "Italy":       {"currency": "EUR", "price": 3800},
            "Japan":       {"currency": "JPY", "price": 623000},
            "Singapore":   {"currency": "SGD", "price": 5900},
            "UK":          {"currency": "GBP", "price": 3250},
            "USA":         {"currency": "USD", "price": 3980},
            "South Korea": {"currency": "KRW", "price": 5400000},
            "UAE":         {"currency": "AED", "price": 14600},
        },
    },

    # ── CELINE ────────────────────────────────────────────────
    {
        "id": 30, "brand": "Celine", "category": "Handbag",
        "product_name": "Classic Box Bag Small",
        "description": "Structured smooth calfskin flap bag — Phoebe Philo's minimalist icon",
        "mytheresa_slug": "celine-classic-box-small",
        "prices": {
            "France":      {"currency": "EUR", "price": 3300},
            "Italy":       {"currency": "EUR", "price": 3300},
            "Japan":       {"currency": "JPY", "price": 541000},
            "Singapore":   {"currency": "SGD", "price": 5100},
            "UK":          {"currency": "GBP", "price": 2820},
            "USA":         {"currency": "USD", "price": 3450},
            "South Korea": {"currency": "KRW", "price": 4690000},
            "UAE":         {"currency": "AED", "price": 12700},
        },
    },
    {
        "id": 31, "brand": "Celine", "category": "Handbag",
        "product_name": "Luggage Nano",
        "description": "Mini structured top-handle tote in smooth calfskin — instantly recognisable",
        "mytheresa_slug": "celine-luggage-nano",
        "prices": {
            "France":      {"currency": "EUR", "price": 2650},
            "Italy":       {"currency": "EUR", "price": 2650},
            "Japan":       {"currency": "JPY", "price": 434000},
            "Singapore":   {"currency": "SGD", "price": 4100},
            "UK":          {"currency": "GBP", "price": 2270},
            "USA":         {"currency": "USD", "price": 2780},
            "South Korea": {"currency": "KRW", "price": 3760000},
            "UAE":         {"currency": "AED", "price": 10170},
        },
    },
    {
        "id": 32, "brand": "Celine", "category": "Handbag",
        "product_name": "16 Bag Small",
        "description": "Hedi Slimane's signature structured flap in grained calfskin",
        "mytheresa_slug": "celine-16-bag-small",
        "prices": {
            "France":      {"currency": "EUR", "price": 2900},
            "Italy":       {"currency": "EUR", "price": 2900},
            "Japan":       {"currency": "JPY", "price": 475000},
            "Singapore":   {"currency": "SGD", "price": 4500},
            "UK":          {"currency": "GBP", "price": 2480},
            "USA":         {"currency": "USD", "price": 3050},
            "South Korea": {"currency": "KRW", "price": 4120000},
            "UAE":         {"currency": "AED", "price": 11130},
        },
    },
    {
        "id": 33, "brand": "Celine", "category": "Handbag",
        "product_name": "Triomphe Canvas Tote",
        "description": "Structured tote in Triomphe canvas with tan leather trim",
        "mytheresa_slug": "celine-triomphe-tote",
        "prices": {
            "France":      {"currency": "EUR", "price": 1650},
            "Italy":       {"currency": "EUR", "price": 1650},
            "Japan":       {"currency": "JPY", "price": 270000},
            "Singapore":   {"currency": "SGD", "price": 2560},
            "UK":          {"currency": "GBP", "price": 1410},
            "USA":         {"currency": "USD", "price": 1730},
            "South Korea": {"currency": "KRW", "price": 2340000},
            "UAE":         {"currency": "AED", "price": 6330},
        },
    },
    {
        "id": 34, "brand": "Celine", "category": "Handbag",
        "product_name": "Ava Bag",
        "description": "Compact semi-rigid crossbody in smooth calfskin with chain strap",
        "mytheresa_slug": "celine-ava-bag",
        "prices": {
            "France":      {"currency": "EUR", "price": 1950},
            "Italy":       {"currency": "EUR", "price": 1950},
            "Japan":       {"currency": "JPY", "price": 319000},
            "Singapore":   {"currency": "SGD", "price": 3050},
            "UK":          {"currency": "GBP", "price": 1670},
            "USA":         {"currency": "USD", "price": 2050},
            "South Korea": {"currency": "KRW", "price": 2770000},
            "UAE":         {"currency": "AED", "price": 7490},
        },
    },
    {
        "id": 35, "brand": "Celine", "category": "Handbag",
        "product_name": "Tabou Clutch",
        "description": "Evening clutch in smooth calfskin with gold Celine lettering",
        "mytheresa_slug": "celine-tabou-clutch",
        "prices": {
            "France":      {"currency": "EUR", "price": 1350},
            "Italy":       {"currency": "EUR", "price": 1350},
            "Japan":       {"currency": "JPY", "price": 221000},
            "Singapore":   {"currency": "SGD", "price": 2100},
            "UK":          {"currency": "GBP", "price": 1160},
            "USA":         {"currency": "USD", "price": 1420},
            "South Korea": {"currency": "KRW", "price": 1920000},
            "UAE":         {"currency": "AED", "price": 5190},
        },
    },
]

# ── Lookup helpers ────────────────────────────────────────────────────────────

def get_product_by_id(product_id: int) -> Dict | None:
    return next((p for p in PRODUCTS if p["id"] == product_id), None)

def get_all_products() -> List[Dict]:
    return PRODUCTS

def get_products_by_brand(brand: str) -> List[Dict]:
    return [p for p in PRODUCTS if p["brand"].lower() == brand.lower()]

def get_all_brands() -> List[str]:
    seen: List[str] = []
    for p in PRODUCTS:
        if p["brand"] not in seen:
            seen.append(p["brand"])
    return seen

def get_all_countries() -> List[str]:
    countries: set = set()
    for p in PRODUCTS:
        countries.update(p["prices"].keys())
    return sorted(countries)
