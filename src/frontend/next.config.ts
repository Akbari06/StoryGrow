import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  // Allow images from placeholder.com for MVP
  images: {
    domains: ['placeholder.com'],
    unoptimized: true, // Required for static export
  },
  // Disable image optimization for static export
  trailingSlash: true,
  // Disable ESLint during builds
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;