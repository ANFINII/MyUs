import { createRequire } from 'module'

const require = createRequire(import.meta.url)
const { i18n } = require('./next-i18next.config.js')

export default {
  reactStrictMode: true,
  reactCompiler: process.env.NODE_ENV === 'production',
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
