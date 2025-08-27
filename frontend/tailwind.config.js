import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        'primary': '#FFFFFF',
        'secondary': '#F3F4F6',
        'accent': '#0070D2',
        'text-primary': '#080707',
        'text-secondary': '#54698D',
        'border': '#DDE5EE',
        'success': '#45C65A',
      }
    },
  },
  plugins: [],
}