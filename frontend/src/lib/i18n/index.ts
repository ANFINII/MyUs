import { initReactI18next } from 'react-i18next'
import { createInstance, i18n } from 'i18next'
import en from './locales/en/common.json'
import ja from './locales/ja/common.json'

export const DEFAULT_LOCALE = 'ja'

const common: Record<string, typeof ja> = { ja, en }

export const createI18n = (locale: string): i18n => {
  const instance = createInstance()
  instance.use(initReactI18next).init({
    lng: locale,
    fallbackLng: DEFAULT_LOCALE,
    defaultNS: 'common',
    resources: Object.fromEntries(Object.entries(common).map(([lng, resource]) => [lng, { common: resource }])),
    interpolation: { escapeValue: false },
    initAsync: false,
  })
  return instance
}
