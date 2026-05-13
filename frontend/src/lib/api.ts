const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ProductCard {
  id: number;
  brand: string;
  product_name: string;
  category: string;
  description: string;
  countries_available: string[];
}

export interface CountryBreakdown {
  country: string;
  currency: string;
  local_price: number;
  vat_refund_rate: number;
  vat_refund_local: number;
  price_after_refund_local: number;
  exchange_rate_to_sgd: number;
  price_after_refund_sgd: number;
  import_gst_sgd: number;
  final_price_sgd: number;
  savings_vs_sg: number;
}

export interface FxMeta {
  source: 'live' | 'fallback' | 'none';
  live_ok: boolean;
  fetched_at: string;   // ISO timestamp
  age_seconds: number;
}

export interface CompareResult {
  product_id: number;
  brand: string;
  product_name: string;
  category: string;
  description: string;
  comparisons: CountryBreakdown[];
  recommendation: string;
  cheapest_country: string;
  cheapest_final_sgd: number;
  price_source: 'scraped' | 'csv' | 'static';
  fx_meta: FxMeta;
}

export interface FxRates {
  rates: Record<string, number>;
  meta: {
    source: string;
    live_ok: boolean;
    fetched_at_iso: string;
    age_seconds: number;
    ttl_seconds: number;
  };
}

export async function searchProducts(query: string): Promise<ProductCard[]> {
  const res = await fetch(
    `${API_URL}/search?q=${encodeURIComponent(query)}`,
    { cache: 'no-store' }
  );
  if (!res.ok) throw new Error('Search failed');
  const data = await res.json();
  return data.results as ProductCard[];
}

export async function compareProduct(productId: number): Promise<CompareResult> {
  const res = await fetch(`${API_URL}/compare/${productId}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Compare failed');
  return res.json() as Promise<CompareResult>;
}

export async function getFxRates(): Promise<FxRates> {
  const res = await fetch(`${API_URL}/fx`, { cache: 'no-store' });
  if (!res.ok) throw new Error('FX fetch failed');
  return res.json() as Promise<FxRates>;
}
