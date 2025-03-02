/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}" // Generally you don't need to list .css here
  ],
  theme: {
    extend: {
      colors: {
        customBlue: '#1fb6ff',
      },
      fontFamily: {
        sans: ['Helvetica', 'Arial', 'sans-serif'],
      },
      fontSize: {
        base: ['16px', '24px'],
        lg: ['18px', '28px'],
      },
    },
  },
  plugins: [],
}