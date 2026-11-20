import { Currency } from 'utils/constants/enum'

export const priceDigits = (currency: Currency): number => new Intl.NumberFormat('en', { style: 'currency', currency }).resolvedOptions().maximumFractionDigits ?? 0

export const formatPrice = (amount: number, currency: Currency, locale: string): string => {
  const format = new Intl.NumberFormat(locale, { style: 'currency', currency })
  return format.format(amount / 10 ** priceDigits(currency))
}

export const priceText = (amount: number, currency: Currency): string => (amount === 0 ? '' : String(amount / 10 ** priceDigits(currency)))

export const priceAmount = (text: string, currency: Currency): number => Math.round(Number(text) * 10 ** priceDigits(currency))

const BLOG_PRICE_MIN = 300
const BLOG_PRICE_MAX = 50000
const COMIC_PRICE_MIN = 300
const COMIC_PRICE_MAX = 5000

export const paidTextError = (paidText: string, price: number): string => {
  if (price < BLOG_PRICE_MIN || price > BLOG_PRICE_MAX) return 'error.priceRange'
  if (paidText === '') return 'error.paidTextRequired'
  return ''
}

export const paidPagesError = (price: number, freePages: number, pageCount: number): string => {
  if (price < COMIC_PRICE_MIN || price > COMIC_PRICE_MAX) return 'error.comicPriceRange'
  if (freePages < 0 || freePages >= pageCount) return 'error.freePagesRange'
  return ''
}
