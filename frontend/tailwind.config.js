/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#eef5ff',
          100: '#daeaff',
          200: '#bdd9ff',
          300: '#90bfff',
          400: '#5c9bff',
          500: '#3373ff',
          600: '#1a52f5',
          700: '#133de1',
          800: '#1633b6',
          900: '#172e8f',
          950: '#111d57',
        },
        accent: {
          400: '#fb923c',
          500: '#f97316',
          600: '#ea6c0c',
        },
      },
      fontFamily: {
        display: ['"Unbounded"', 'sans-serif'],
        body: ['"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease forwards',
        'slide-up': 'slideUp 0.5s ease forwards',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
