import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f7ff",
          100: "#e0effe",
          500: "#3b82f6",
          600: "#2563eb",
          900: "#1e3a8a",
        },
        surface: {
          50: "#fafafa",
          100: "#f5f5f5",
          900: "#171717",
        }
      },
      borderRadius: {
        'gv': '12px',
      }
    },
  },
  plugins: [],
};
export default config;