/** @type {import('next').NextConfig} */

import { createRequire } from 'module'

const require = createRequire(import.meta.url)
const { i18n } = require('./next-i18next.config.js')

export default {
  reactStrictMode: true,
  reactCompiler: true,
  basePath: '',
  i18n,
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: '127.0.0.1' },
      { protocol: 'https', hostname: 'my-us.vercel.app' },
    ],
    formats: ['image/avif', 'image/webp'],
  },
}
