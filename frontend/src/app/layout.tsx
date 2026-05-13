import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'LuxCompare AI — Global Luxury Price Comparison',
  description:
    'Compare luxury goods prices across France, Italy, Japan & Singapore after VAT refunds, currency conversion and import GST.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-ivory">
        {children}
      </body>
    </html>
  );
}
