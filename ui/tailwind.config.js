/** @type {import('tailwindcss').Config} */
module.exports = {
  prefix: "tw-",
  corePlugins: {
    preflight: false,
  },
  purge: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  content: [],
  theme: {
    extend: {
      colors: {
        blue: {
          50: "#EDF8FF",
          100: "#D6EFFF",
          200: "#B5E4FF",
          300: "#83D5FF",
          400: "#48BCFF",
          500: "#1E9AFF",
          600: "#067AFF",
          700: "#0066FF",
          800: "#084EC5",
          900: "#0D469B",
          950: "#0E2B5D",
        },
      },
    },
  },
  plugins: [require("tailwindcss-primeui")],
};
