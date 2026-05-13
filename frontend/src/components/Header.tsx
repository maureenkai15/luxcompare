'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="w-full border-b border-gold/20 bg-ivory/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link href="/" className="group flex flex-col leading-none">
          <span className="font-serif text-2xl font-light tracking-widest text-obsidian-900 uppercase">
            LuxCompare
          </span>
          <span className="font-mono text-[9px] tracking-widest2 text-gold-400 uppercase mt-0.5">
            Global Price Intelligence
          </span>
        </Link>

        <nav className="flex items-center gap-8">
          <span className="font-sans text-xs tracking-widest uppercase text-obsidian-700/50 select-none">
            France · Italy · Japan · Singapore
          </span>
        </nav>
      </div>
    </header>
  );
}
