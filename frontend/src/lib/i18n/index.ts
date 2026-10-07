import { initReactI18next } from 'react-i18next'
import { createInstance, i18n } from 'i18next'
import enAccount from './locales/en/account.json'
import enCommon from './locales/en/common.json'
import enManage from './locales/en/manage.json'
import enMedia from './locales/en/media.json'
import enMenu from './locales/en/menu.json'
import enSetting from './locales/en/setting.json'
import jaAccount from './locales/ja/account.json'
import jaCommon from './locales/ja/common.json'
import jaManage from './locales/ja/manage.json'
import jaMedia from './locales/ja/media.json'
import jaMenu from './locales/ja/menu.json'
import jaSetting from './locales/ja/setting.json'

export const DEFAULT_LOCALE = 'ja'
export const LOCALES = ['en']

export const resources = {
  ja: { common: jaCommon, account: jaAccount, setting: jaSetting, manage: jaManage, menu: jaMenu, media: jaMedia },
  en: { common: enCommon, account: enAccount, setting: enSetting, manage: enManage, menu: enMenu, media: enMedia },
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
