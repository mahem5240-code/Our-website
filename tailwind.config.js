/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"SF Pro Display"', '"Inter"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        text: ['"SF Pro Text"', '"Inter"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      colors: {
        canvas: {
          light: '#F5F5F7',
          dark: '#000000',
        },
        surface: {
          light: '#FFFFFF',
          dark: '#1C1C1E',
        },
        ink: {
          light: '#1D1D1F',
          dark: '#F5F5F7',
        },
        muted: {
          light: '#6E6E73',
          dark: '#98989D',
        },
        line: {
          light: '#E5E5EA',
          dark: '#2C2C2E',
        },
        accent: {
          blue: '#0071E3',
          indigo: '#5E5CE6',
          teal: '#0AB8B0',
          orange: '#FF9F0A',
          pink: '#FF375F',
          green: '#30D158',
          purple: '#BF5AF2',
        },
      },
      borderRadius: {
        xl2: '1.25rem',
        xl3: '1.75rem',
      },
      boxShadow: {
        soft: '0 1px 2px rgba(0,0,0,0.04), 0 8px 24px -8px rgba(0,0,0,0.08)',
        softDark: '0 1px 2px rgba(0,0,0,0.3), 0 8px 24px -8px rgba(0,0,0,0.5)',
        glow: '0 0 0 1px rgba(255,255,255,0.06)',
      },
      backdropBlur: {
        xs: '2px',
      },
      keyframes: {
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.55 },
        },
      },
      animation: {
        shimmer: 'shimmer 1.6s infinite',
        pulseSoft: 'pulseSoft 2.2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
