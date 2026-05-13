'use client';

import { useState, useEffect, useRef } from 'react';
import { Search, X } from 'lucide-react';
import { searchProducts, ProductCard } from '@/lib/api';

interface SearchBarProps {
  onSelect: (product: ProductCard) => void;
}

const BRANDS = ['Chanel', 'Louis Vuitton', 'Dior', 'Hermès'];

export default function SearchBar({ onSelect }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<ProductCard[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setOpen(false);
      return;
    }
    const t = setTimeout(async () => {
      setLoading(true);
      try {
        const r = await searchProducts(query);
        setResults(r);
        setOpen(true);
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 280);
    return () => clearTimeout(t);
  }, [query]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSelect = (p: ProductCard) => {
    setQuery(`${p.brand} — ${p.product_name}`);
    setOpen(false);
    onSelect(p);
  };

  const handleChipClick = async (brand: string) => {
    setQuery(brand);
    setLoading(true);
    try {
      const r = await searchProducts(brand);
      setResults(r);
      setOpen(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div ref={ref} className="relative w-full max-w-2xl mx-auto">
      <div className="relative group">
        <Search
          size={16}
          className="absolute left-5 top-1/2 -translate-y-1/2 text-gold-400"
        />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => { if (results.length) setOpen(true); }}
          placeholder="Search by brand or product — e.g. Birkin 25, Lady Dior"
          className="w-full pl-12 pr-12 py-4 bg-white border border-gold/30 rounded-none font-sans text-sm text-obsidian-900 placeholder-obsidian-700/30 focus:outline-none focus:border-gold-400 transition-colors duration-200 shadow-sm"
        />
        {query && (
          <button
            onClick={() => { setQuery(''); setResults([]); setOpen(false); }}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-obsidian-700/30 hover:text-gold-400 transition-colors"
          >
            <X size={14} />
          </button>
        )}
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gold scale-x-0 group-focus-within:scale-x-100 transition-transform duration-300 origin-left" />
      </div>

      <div className="flex gap-2 mt-3 flex-wrap justify-center">
        {BRANDS.map((b) => (
          <button
            key={b}
            onClick={() => handleChipClick(b)}
            className="px-3 py-1 border border-gold/30 text-[10px] tracking-widest uppercase font-sans text-obsidian-700/60 hover:border-gold-400 hover:text-gold-400 transition-all duration-200"
          >
            {b}
          </button>
        ))}
      </div>

      {open && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gold/20 shadow-xl z-50 max-h-80 overflow-y-auto">
          {loading && (
            <div className="px-5 py-4 text-xs text-obsidian-700/40 font-sans tracking-wide animate-pulse">
              Searching…
            </div>
          )}
          {!loading && results.length === 0 && (
            <div className="px-5 py-4 text-xs text-obsidian-700/40 font-sans">
              No products found.
            </div>
          )}
          {!loading && results.map((p) => (
            <button
              key={p.id}
              onClick={() => handleSelect(p)}
              className="w-full text-left px-5 py-3 hover:bg-stone-50 border-b border-gold/10 last:border-b-0 transition-colors duration-150"
            >
              <div className="flex items-baseline justify-between gap-3">
                <div>
                  <span className="font-mono text-[9px] tracking-widest uppercase text-gold-400 mr-2">
                    {p.brand}
                  </span>
                  <span className="font-serif text-base text-obsidian-900">
                    {p.product_name}
                  </span>
                </div>
                <span className="text-[9px] tracking-widest uppercase text-obsidian-700/30 font-sans shrink-0">
                  {p.countries_available.length} countries
                </span>
              </div>
              <p className="text-[11px] text-obsidian-700/40 font-sans mt-0.5 line-clamp-1">
                {p.description}
              </p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
