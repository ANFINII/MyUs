import ja from 'lib/i18n/locales/ja/common.json'

declare module 'i18next' {
  interface CustomTypeOptions {
    defaultNS: 'common'
    resources: { common: typeof ja }
  }
}
