export default {
  reactStrictMode: true,
  reactCompiler: true,
  agentRules: false,
  basePath: '',
  i18n: {
    defaultLocale: 'ja',
    locales: ['ja', 'en'],
  },
  sassOptions: {
    implementation: 'sass-embedded',
  },
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: '127.0.0.1' },
      { protocol: 'https', hostname: 'my-us.vercel.app' },
    ],
    formats: ['image/avif', 'image/webp'],
  },
}
