/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable @typescript-eslint/explicit-function-return-type */
/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
}

const { i18n } = require('./next-i18next.config')

module.exports = {
  nextConfig,
  i18n,
  images: { domains: ['127.0.0.1'], formats: ['image/avif', 'image/webp'] },
}
