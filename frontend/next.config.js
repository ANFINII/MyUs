/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable @typescript-eslint/explicit-function-return-type */
/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  basePath: '',
  images: {
    domains: ['www.google.com'],
  },
  async redirects() {
    return [{ source: '/', destination: '/', permanent: true }]
  },
}

const { i18n } = require('./next-i18next.config')

module.exports = {
  nextConfig,
  i18n,
  images: { domains: ['127.0.0.1', 'https://my-us.vercel.app/'], formats: ['image/avif', 'image/webp'] },
}
