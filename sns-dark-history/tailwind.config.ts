module.exports = {
  theme: {
    extend: {
      backgroundImage: () => ({
        "back-img": "url('../img/background1.PNG')",
      }),
    },
  },
};

import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
export default config;
