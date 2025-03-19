import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: {
    serverMinification: false,
    proxyTimeout: 1000 * 120,
  },
  async rewrites() {
    return [
      {
        source: '/api/posts/:user_id',
        destination: 'http://backend:5001/posts/:user_id',
      },
      {
        source: '/api/dark_posts/:user_id',
        destination: 'http://backend:5001/dark_posts/:user_id',
      },
      {
        source: '/api/post',
        destination: 'http://backend:5001/post',
      },
    ]
  },
}

module.exports = nextConfig
