import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow images from placeholder.com for MVP
  images: {
    domains: ['placeholder.com'],
  },
  // Handle CORS for API calls
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ]
  },
};

export default nextConfig;