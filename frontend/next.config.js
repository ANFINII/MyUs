/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    reactCompiler: true,
  },
  basePath: '',
  images: {
    domains: ['www.google.com'],
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  async redirects() {
    return [{ source: '/', destination: '/', permanent: true }]
  },
}

const { i18n } = require('./next-i18next.config')

module.exports = {
  ...nextConfig,
  i18n,
  images: {
    domains: ['127.0.0.1', 'my-us.vercel.app'],
    formats: ['image/avif', 'image/webp']
  },
}
