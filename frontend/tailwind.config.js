/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aws: {
          squid: '#232f3e',
          smile: '#ff9900',
          anchor: '#0073bb',
          charcoal: '#131921',
          lightgray: '#eaeded',
          border: '#e5e7eb',
          card: '#ffffff',
          darkbg: '#0f172a'
        }
      }
    },
  },
  plugins: [],
}
