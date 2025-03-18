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
        destination: 'http://backend:5001/dark_posts/:user_id',
      },
      {
        source: '/api/post',
        destination: 'http://backend:5001/post',
      },
      {
        source: '/api/icon/:user_id',
        destination: 'http://backend:5001/icon/:user_id',
      },
    ]
  },
}

module.exports = nextConfig
