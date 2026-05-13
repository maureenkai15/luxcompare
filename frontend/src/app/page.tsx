'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import SearchBar from '@/components/SearchBar';
import ComparisonTable from '@/components/ComparisonTable';
import RecommendationCard from '@/components/RecommendationCard';
import PriceBreakdown from '@/components/PriceBreakdown';
import FxStatus from '@/components/FxStatus';
import PriceSourceBadge from '@/components/PriceSourceBadge';
import { ProductCard, CompareResult, compareProduct } from '@/lib/api';
import { Loader2 } from 'lucide-react';

const FEATURED_BRANDS = [
  { name: 'Chanel',        tagline: 'Classic Flap · Boy Bag · Gabrielle' },
  { name: 'Louis Vuitton', tagline: 'Neverfull · Capucines · Twist' },
  { name: 'Dior',          tagline: 'Lady Dior · Book Tote · Saddle' },
  { name: 'Hermès',        tagline: 'Birkin · Kelly · Constance' },
];

export default function HomePage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CompareResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSelect(product: ProductCard) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await compareProduct(product.id);
      setResult(data);
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch {
      setError('Unable to load comparison. Please ensure the backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  }

  const topSaving = result?.comparisons.find(
    c => c.country === result.cheapest_country
  )?.savings_vs_sg ?? 0;

  return (
    <div className="min-h-screen flex flex-col bg-ivory-50">
      <Header />

      {/* ── Hero ── */}
      <section className="relative flex flex-col items-center justify-center px-6 pt-20 pb-16 overflow-hidden">
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full border border-gold/5" />
          <div className="absolute top-16 left-1/2 -translate-x-1/2 w-[440px] h-[440px] rounded-full border border-gold/8" />
          <div
            className="absolute -top-20 right-10 w-64 h-64 opacity-5"
            style={{
              backgroundImage: `repeating-linear-gradient(45deg, #c49a50 0, #c49a50 1px, transparent 0, transparent 50%)`,
              backgroundSize: '12px 12px',
            }}
          />
        </div>

        <div className="relative text-center max-w-3xl mx-auto">
          <p className="font-mono text-[10px] tracking-widest3 uppercase text-gold-400 mb-6 fade-up">
            Global Luxury · Price Intelligence
          </p>
          <h1 className="font-serif text-5xl md:text-7xl text-obsidian-900 leading-none mb-6 fade-up fade-up-delay-1">
            Buy Smarter,<br />
            <span className="italic gold-shimmer">Buy Cheaper.</span>
          </h1>
          <p className="font-sans text-sm md:text-base text-obsidian-700/50 max-w-lg mx-auto mb-10 leading-relaxed fade-up fade-up-delay-2">
            Compare luxury goods prices across France, Italy, Japan & Singapore —
            after VAT refunds, currency conversion, and Singapore import GST.
          </p>

          <div className="fade-up fade-up-delay-3">
            <SearchBar onSelect={handleSelect} />
          </div>

          {/* Global FX status bar */}
          <div className="mt-6 flex justify-center fade-up fade-up-delay-4">
            <FxStatus />
          </div>
        </div>
      </section>

      {/* ── Brand grid (shown when no results) ── */}
      {!result && !loading && (
        <section className="max-w-4xl mx-auto px-6 pb-16 w-full">
          <div className="divider-gold mb-10" />
          <p className="font-mono text-[9px] tracking-widest uppercase text-obsidian-700/30 text-center mb-6">
            Featured Houses
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {FEATURED_BRANDS.map((b, i) => (
              <div
                key={b.name}
                className={`border border-gold/20 p-5 text-center hover:border-gold-400
                            transition-all duration-200 cursor-default group
                            fade-up fade-up-delay-${Math.min(i + 1, 4)}`}
              >
                <div className="font-serif text-lg text-obsidian-900 mb-1 group-hover:text-gold-500 transition-colors">
                  {b.name}
                </div>
                <div className="font-mono text-[8px] tracking-wide text-obsidian-700/30 leading-relaxed">
                  {b.tagline}
                </div>
              </div>
            ))}
          </div>

          <div className="divider-gold my-10" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            {[
              { step: '01', title: 'Search',  desc: 'Find your desired luxury item by brand or name' },
              { step: '02', title: 'Compare', desc: 'View live VAT-adjusted prices across 4 countries' },
              { step: '03', title: 'Save',    desc: 'Identify where to buy to maximise your savings' },
            ].map(s => (
              <div key={s.step} className="space-y-2">
                <div className="font-mono text-[9px] tracking-widest text-gold-400">{s.step}</div>
                <div className="font-serif text-xl text-obsidian-900">{s.title}</div>
                <div className="font-sans text-xs text-obsidian-700/40 leading-relaxed">{s.desc}</div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ── Loading ── */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-24 gap-4">
          <Loader2 size={24} className="animate-spin text-gold-400" />
          <p className="font-mono text-xs tracking-widest text-obsidian-700/40 uppercase animate-pulse">
            Fetching live rates & calculating…
          </p>
        </div>
      )}

      {/* ── Error ── */}
      {error && (
        <div className="max-w-2xl mx-auto px-6 pb-12">
          <div className="border border-rose-200 bg-rose-50 px-6 py-4 text-sm font-sans text-rose-600">
            {error}
          </div>
        </div>
      )}

      {/* ── Results ── */}
      {result && !loading && (
        <section id="results" className="max-w-5xl mx-auto px-6 pb-20 w-full space-y-8">
          <div className="divider-gold" />

          {/* Product header */}
          <div className="fade-up">
            <p className="font-mono text-[10px] tracking-widest uppercase text-gold-400 mb-1">
              {result.brand}
            </p>
            <h2 className="font-serif text-3xl md:text-4xl text-obsidian-900">
              {result.product_name}
            </h2>
            <p className="font-sans text-sm text-obsidian-700/40 mt-2">{result.description}</p>

            {/* Data provenance row */}
            <div className="flex flex-wrap items-center gap-3 mt-4">
              <PriceSourceBadge source={result.price_source} />
              <FxStatus initialMeta={result.fx_meta} />
            </div>
          </div>

          {/* Recommendation */}
          <RecommendationCard
            recommendation={result.recommendation}
            cheapestCountry={result.cheapest_country}
            cheapestFinalSgd={result.cheapest_final_sgd}
            savingsVsSg={topSaving}
          />

          {/* Main comparison table */}
          <div className="border border-gold/20 bg-white fade-up">
            <div className="px-5 py-4 border-b border-gold/10 flex flex-wrap items-center justify-between gap-2">
              <h3 className="font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40">
                Country Comparison
              </h3>
              <span className="font-mono text-[9px] tracking-widest uppercase text-gold-400">
                All prices in SGD after duties
              </span>
            </div>
            <ComparisonTable
              comparisons={result.comparisons}
              cheapestCountry={result.cheapest_country}
            />
          </div>

          {/* Breakdown accordion */}
          <div className="fade-up">
            <PriceBreakdown comparisons={result.comparisons} />
          </div>

          {/* Disclaimer */}
          <p className="font-sans text-[10px] text-obsidian-700/25 text-center leading-relaxed fade-up">
            Prices are indicative and based on manually curated data. VAT refund rates, exchange rates,
            and import duties may vary. Always verify with the retailer and Singapore Customs before purchasing.
            FX rates sourced from open.er-api.com.
          </p>
        </section>
      )}

      {/* ── Footer ── */}
      <footer className="mt-auto border-t border-gold/10 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-3">
          <span className="font-serif text-lg text-obsidian-700/30">LuxCompare AI</span>
          <FxStatus />
          <span className="font-mono text-[9px] tracking-widest uppercase text-obsidian-700/20">
            For informational purposes only · Not financial advice
          </span>
        </div>
      </footer>
    </div>
  );
}
