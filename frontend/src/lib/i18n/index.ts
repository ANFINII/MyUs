import { initReactI18next } from 'react-i18next'
import { createInstance, i18n } from 'i18next'
import en from './locales/en/common.json'
import ja from './locales/ja/common.json'

export const DEFAULT_LOCALE = 'ja'
export const LOCALES = ['en']

export const getLocale = (path: string): string | undefined => {
  const first = path.split(/[/?#]/)[1] ?? ''
  return LOCALES.includes(first) ? first : undefined
}

export const resources = {
  ja: { common: ja },
  en: { common: en },
}

export const createI18n = (locale: string): i18n => {
  const instance = createInstance()
  instance.use(initReactI18next).init({
    lng: locale,
    fallbackLng: DEFAULT_LOCALE,
    defaultNS: 'common',
    resources,
    interpolation: { escapeValue: false },
    initAsync: false,
  })
  return instance
}
