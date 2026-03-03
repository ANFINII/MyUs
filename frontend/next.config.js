/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  reactCompiler: true,
  basePath: '',
  async redirects() {
    return [{ source: '/', destination: '/', permanent: true }]
  },
}

const { i18n } = require('./next-i18next.config')

module.exports = {
  ...nextConfig,
  i18n,
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: '127.0.0.1' },
      { protocol: 'https', hostname: 'my-us.vercel.app' },
    ],
    formats: ['image/avif', 'image/webp'],
  },
}
