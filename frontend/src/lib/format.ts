const FLAGS: Record<string, string> = {
  France: '🇫🇷',
  Italy: '🇮🇹',
  Japan: '🇯🇵',
  Singapore: '🇸🇬',
};

export function getFlag(country: string): string {
  return FLAGS[country] ?? '🌍';
}

export function formatSGD(amount: number): string {
  return new Intl.NumberFormat('en-SG', {
    style: 'currency',
    currency: 'SGD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatLocal(amount: number, currency: string): string {
  return new Intl.NumberFormat('en', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}
