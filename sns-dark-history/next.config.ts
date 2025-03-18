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
        source: '/api/:subpath',
        destination: 'http://backend:5001/:subpath',
      },
    ]
  },
}

module.exports = nextConfig
