'use client';

import { useEffect, useState } from 'react';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';
import { getFxRates, FxRates } from '@/lib/api';

function formatAge(seconds: number): string {
  if (seconds < 60)  return `${Math.round(seconds)}s ago`;
  if (seconds < 3600) return `${Math.round(seconds / 60)}m ago`;
  return `${Math.round(seconds / 3600)}h ago`;
}

function formatTime(iso: string): string {
  if (!iso || iso === 'never') return '—';
  try {
    return new Date(iso).toLocaleTimeString('en-SG', {
      hour:   '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZone: 'Asia/Singapore',
    });
  } catch { return iso; }
}

interface Props {
  /** If a compare result already carries fx_meta, pass it to skip an extra fetch */
  initialMeta?: {
    source: string;
    live_ok: boolean;
    fetched_at: string;
    age_seconds: number;
  } | null;
}

export default function FxStatus({ initialMeta = null }: Props) {
  const [data, setData] = useState<FxRates | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!initialMeta) load();
  }, [initialMeta]);

  async function load() {
    setLoading(true);
    try {
      const fx = await getFxRates();
      setData(fx);
    } catch {
      // silently fail — status indicator is non-critical
    } finally {
      setLoading(false);
    }
  }

  const meta = initialMeta ?? data?.meta;
  const isLive = meta?.live_ok ?? false;
  const source = meta?.source ?? 'unknown';
  const timestamp = initialMeta
    ? formatTime(initialMeta.fetched_at)
    : data
    ? formatTime(data.meta.fetched_at_iso)
    : '—';
  const age = meta?.age_seconds ?? 0;

  // Key rates to display
  const rates = data?.rates;

  return (
    <div className="flex flex-wrap items-center gap-4 text-[10px] font-mono">
      {/* Live / Fallback badge */}
      <div className={`flex items-center gap-1.5 px-2 py-1 border ${
        isLive
          ? 'border-emerald-300 bg-emerald-50 text-emerald-600'
          : 'border-amber-300 bg-amber-50 text-amber-600'
      }`}>
        {isLive
          ? <Wifi size={10} />
          : <WifiOff size={10} />
        }
        <span className="tracking-widest uppercase">
          {isLive ? 'Live FX' : 'Fallback FX'}
        </span>
      </div>

      {/* Timestamp */}
      {meta && (
        <span className="text-obsidian-700/30 tracking-wide">
          Updated {formatAge(age)} · {timestamp} SGT
        </span>
      )}

      {/* Key rates */}
      {rates && (
        <div className="flex items-center gap-3 text-obsidian-700/40">
          {['EUR', 'JPY', 'GBP'].map(cur => (
            rates[cur] ? (
              <span key={cur}>
                1 {cur} ={' '}
                <span className="text-obsidian-900">
                  S${cur === 'JPY'
                    ? rates[cur].toFixed(4)
                    : rates[cur].toFixed(4)}
                </span>
              </span>
            ) : null
          ))}
        </div>
      )}

      {/* Refresh button */}
      {!initialMeta && (
        <button
          onClick={load}
          disabled={loading}
          className="text-gold-400 hover:text-gold-500 transition-colors disabled:opacity-30"
          title="Refresh FX rates"
        >
          <RefreshCw size={10} className={loading ? 'animate-spin' : ''} />
        </button>
      )}
    </div>
  );
}
