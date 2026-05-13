'use client';

import { getFlag, formatSGD } from '@/lib/format';
import { MapPin } from 'lucide-react';

interface RecommendationCardProps {
  recommendation: string;
  cheapestCountry: string;
  cheapestFinalSgd: number;
  savingsVsSg: number;
}

export default function RecommendationCard({
  recommendation,
  cheapestCountry,
  cheapestFinalSgd,
  savingsVsSg,
}: RecommendationCardProps) {
  return (
    <div className="relative border border-gold/30 bg-white p-6 md:p-8 fade-up">
      {/* Corner ornament */}
      <div className="absolute top-0 left-0 w-6 h-6 border-t border-l border-gold/60" />
      <div className="absolute top-0 right-0 w-6 h-6 border-t border-r border-gold/60" />
      <div className="absolute bottom-0 left-0 w-6 h-6 border-b border-l border-gold/60" />
      <div className="absolute bottom-0 right-0 w-6 h-6 border-b border-r border-gold/60" />

      <div className="flex flex-col md:flex-row md:items-center gap-6">
        {/* Country badge */}
        <div className="flex-shrink-0 flex flex-col items-center justify-center
                        w-24 h-24 border border-gold/30 bg-ivory-100">
          <span className="text-4xl leading-none">{getFlag(cheapestCountry)}</span>
          <span className="font-mono text-[9px] tracking-widest uppercase text-gold-400 mt-2">
            Best Buy
          </span>
        </div>

        {/* Text */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-3">
            <MapPin size={12} className="text-gold-400" />
            <span className="font-mono text-[9px] tracking-widest uppercase text-gold-400">
              AI Recommendation
            </span>
          </div>
          <p className="font-serif text-lg md:text-xl text-obsidian-900 leading-relaxed italic">
            "{recommendation}"
          </p>
        </div>

        {/* Savings */}
        {savingsVsSg > 0 && (
          <div className="flex-shrink-0 text-center md:text-right">
            <div className="font-mono text-[9px] tracking-widest uppercase text-obsidian-700/40 mb-1">
              You Save
            </div>
            <div className="font-serif text-3xl text-gold-500">
              {formatSGD(savingsVsSg)}
            </div>
            <div className="font-mono text-[9px] tracking-widest text-obsidian-700/30 mt-1">
              vs buying in Singapore
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
