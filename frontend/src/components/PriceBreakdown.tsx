'use client';

import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { CountryBreakdown } from '@/lib/api';
import { getFlag, formatSGD, formatLocal } from '@/lib/format';

interface PriceBreakdownProps {
  comparisons: CountryBreakdown[];
}

export default function PriceBreakdown({ comparisons }: PriceBreakdownProps) {
  const [open, setOpen] = useState<string | null>(null);

  return (
    <div className="border border-gold/20 divide-y divide-gold/10">
      <div className="px-5 py-3 bg-ivory-100">
        <h3 className="font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40">
          Detailed Price Breakdown
        </h3>
      </div>
      {comparisons.map(row => (
        <div key={row.country}>
          <button
            onClick={() => setOpen(open === row.country ? null : row.country)}
            className="w-full flex items-center justify-between px-5 py-3
                       hover:bg-ivory-100 transition-colors duration-150 text-left"
          >
            <div className="flex items-center gap-3">
              <span className="text-base">{getFlag(row.country)}</span>
              <span className="font-serif text-sm text-obsidian-900">{row.country}</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="font-mono text-sm text-obsidian-900">
                {formatSGD(row.final_price_sgd)}
              </span>
              <ChevronDown
                size={14}
                className={`text-gold-400 transition-transform duration-200 ${
                  open === row.country ? 'rotate-180' : ''
                }`}
              />
            </div>
          </button>

          {open === row.country && (
            <div className="px-5 pb-4 bg-ivory-50 space-y-2">
              <Row label="Retail price (local)" value={formatLocal(row.local_price, row.currency)} />
              <Row
                label={`VAT refund (${(row.vat_refund_rate * 100).toFixed(0)}%)`}
                value={row.vat_refund_local > 0 ? `−${formatLocal(row.vat_refund_local, row.currency)}` : '—'}
                accent="green"
              />
              <Row
                label={`After refund (at 1 ${row.currency} = S$${row.exchange_rate_to_sgd})`}
                value={formatSGD(row.price_after_refund_sgd)}
              />
              <Row
                label="Singapore import GST (9%)"
                value={row.import_gst_sgd > 0 ? `+${formatSGD(row.import_gst_sgd)}` : '—'}
                accent="red"
              />
              <div className="divider-gold my-2" />
              <Row label="Final landed cost (SGD)" value={formatSGD(row.final_price_sgd)} bold />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function Row({
  label,
  value,
  accent,
  bold,
}: {
  label: string;
  value: string;
  accent?: 'green' | 'red';
  bold?: boolean;
}) {
  const valClass =
    accent === 'green'
      ? 'text-emerald-600'
      : accent === 'red'
      ? 'text-rose-400'
      : bold
      ? 'text-gold-500 font-medium'
      : 'text-obsidian-900';

  return (
    <div className="flex justify-between items-center text-xs py-0.5">
      <span className="font-sans text-obsidian-700/50">{label}</span>
      <span className={`font-mono ${valClass}`}>{value}</span>
    </div>
  );
}
