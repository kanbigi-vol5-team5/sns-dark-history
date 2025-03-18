import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: {
    serverMinification: false,
    proxyTimeout: 1000 * 120,
  },
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/dark_posts/:user_id',
        destination: 'http://100.72.123.53:5001/dark_posts/:user_id',
      },
      {
        source: '/api/post',
        destination: 'http://100.66.228.90:5001/post',
      },
      {
        source: '/api/icon',
        destination: 'http://100.66.228.90:5001/icon',
      },
    ]
  },
}

module.exports = nextConfig
