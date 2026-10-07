import { resources } from 'lib/i18n'

declare module 'i18next' {
  interface CustomTypeOptions {
    defaultNS: 'common'
    resources: (typeof resources)['ja']
  }
}
