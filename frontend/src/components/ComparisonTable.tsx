'use client';

import { CountryBreakdown } from '@/lib/api';
import { getFlag, formatSGD, formatLocal } from '@/lib/format';
import { TrendingDown, Minus } from 'lucide-react';

interface ComparisonTableProps {
  comparisons: CountryBreakdown[];
  cheapestCountry: string;
}

export default function ComparisonTable({ comparisons, cheapestCountry }: ComparisonTableProps) {
  return (
    <div className="w-full overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="border-b border-gold/20">
            <th className="text-left py-3 px-4 font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40 font-normal">
              Country
            </th>
            <th className="text-right py-3 px-4 font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40 font-normal">
              Local Price
            </th>
            <th className="text-right py-3 px-4 font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40 font-normal hidden sm:table-cell">
              VAT Refund
            </th>
            <th className="text-right py-3 px-4 font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40 font-normal hidden md:table-cell">
              Import GST
            </th>
            <th className="text-right py-3 px-4 font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40 font-normal">
              Final (SGD)
            </th>
            <th className="text-right py-3 px-4 font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40 font-normal">
              vs SG
            </th>
          </tr>
        </thead>
        <tbody>
          {comparisons.map((row, i) => {
            const isCheapest = row.country === cheapestCountry;
            const isSG = row.country === 'Singapore';
            const saving = row.savings_vs_sg;

            return (
              <tr
                key={row.country}
                className={`
                  border-b border-gold/10 transition-colors duration-150
                  ${isCheapest ? 'bg-gold/5' : 'hover:bg-ivory-100'}
                  fade-up fade-up-delay-${Math.min(i + 1, 4)}
                `}
              >
                {/* Country */}
                <td className="py-4 px-4">
                  <div className="flex items-center gap-2.5">
                    <span className="text-lg leading-none">{getFlag(row.country)}</span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className={`font-serif text-base ${isCheapest ? 'text-gold-500' : 'text-obsidian-900'}`}>
                          {row.country}
                        </span>
                        {isCheapest && (
                          <span className="text-[8px] tracking-widest uppercase font-mono
                                          bg-gold text-white px-1.5 py-0.5">
                            Best
                          </span>
                        )}
                      </div>
                      <div className="text-[10px] font-mono text-obsidian-700/30 mt-0.5">
                        Rate: {(row.vat_refund_rate * 100).toFixed(0)}% refund
                        {' · '}1 {row.currency} = S${row.exchange_rate_to_sgd.toFixed(4)}
                      </div>
                    </div>
                  </div>
                </td>

                {/* Local Price */}
                <td className="py-4 px-4 text-right font-mono text-sm text-obsidian-900">
                  {formatLocal(row.local_price, row.currency)}
                </td>

                {/* VAT Refund */}
                <td className="py-4 px-4 text-right font-mono text-sm hidden sm:table-cell">
                  {row.vat_refund_local > 0 ? (
                    <span className="text-emerald-600">
                      −{formatLocal(row.vat_refund_local, row.currency)}
                    </span>
                  ) : (
                    <span className="text-obsidian-700/20">—</span>
                  )}
                </td>

                {/* Import GST */}
                <td className="py-4 px-4 text-right font-mono text-sm hidden md:table-cell">
                  {row.import_gst_sgd > 0 ? (
                    <span className="text-rose-400">
                      +{formatSGD(row.import_gst_sgd)}
                    </span>
                  ) : (
                    <span className="text-obsidian-700/20">—</span>
                  )}
                </td>

                {/* Final SGD */}
                <td className="py-4 px-4 text-right">
                  <span className={`font-mono text-base font-medium ${isCheapest ? 'text-gold-500' : 'text-obsidian-900'}`}>
                    {formatSGD(row.final_price_sgd)}
                  </span>
                </td>

                {/* Savings vs SG */}
                <td className="py-4 px-4 text-right">
                  {isSG ? (
                    <span className="text-obsidian-700/20 font-mono text-xs">baseline</span>
                  ) : saving > 0 ? (
                    <span className="flex items-center justify-end gap-1 text-emerald-600 font-mono text-sm">
                      <TrendingDown size={12} />
                      {formatSGD(saving)}
                    </span>
                  ) : saving < 0 ? (
                    <span className="font-mono text-sm text-rose-400">
                      +{formatSGD(Math.abs(saving))}
                    </span>
                  ) : (
                    <Minus size={12} className="ml-auto text-obsidian-700/20" />
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
