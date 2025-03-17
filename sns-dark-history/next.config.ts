import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/dark_posts/:user_id',
        destination: 'http://100.72.123.53:5001/dark_posts/:user_id',
      },
    ]
  },
}

module.exports = nextConfig
