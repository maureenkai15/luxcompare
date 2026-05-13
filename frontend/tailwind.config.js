/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Cormorant Garamond', 'Georgia', 'serif'],
        sans: ['DM Sans', 'system-ui', 'sans-serif'],
        mono: ['DM Mono', 'monospace'],
      },
      colors: {
        ivory: {
          50:  '#fdfcf8',
          100: '#f9f7f0',
          200: '#f3efe4',
        },
        gold: {
          300: '#d4af70',
          400: '#c49a50',
          500: '#a07830',
          600: '#7a5c20',
        },
        obsidian: {
          900: '#0d0d0d',
          800: '#1a1a1a',
          700: '#252525',
        },
      },
      letterSpacing: {
        widest2: '0.25em',
        widest3: '0.35em',
      },
    },
  },
  plugins: [],
};
