 
const path = require('path')

module.exports = {
  i18n: {
    defaultLocale: 'ja',
    locales: ['ja', 'en'],
  },
  localePath: typeof window === 'undefined' ? path.resolve('./public/locales') : '/locales',
}
