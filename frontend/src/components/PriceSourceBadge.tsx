'use client';

interface Props {
  source: 'scraped' | 'csv' | 'static' | string;
}

const SOURCE_CONFIG: Record<string, { label: string; color: string }> = {
  scraped: { label: 'Live scraped',  color: 'border-violet-300 bg-violet-50 text-violet-600' },
  csv:     { label: 'CSV override',  color: 'border-blue-300 bg-blue-50 text-blue-600' },
  static:  { label: 'Manual data',  color: 'border-stone-200 bg-stone-50 text-stone-400' },
};

export default function PriceSourceBadge({ source }: Props) {
  const cfg = SOURCE_CONFIG[source] ?? SOURCE_CONFIG.static;
  return (
    <span className={`inline-flex items-center px-2 py-0.5 border text-[9px] font-mono tracking-widest uppercase ${cfg.color}`}>
      {cfg.label}
    </span>
  );
}
