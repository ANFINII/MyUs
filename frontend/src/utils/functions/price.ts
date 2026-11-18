import { Currency } from 'utils/constants/enum'

export const priceDigits = (currency: Currency): number => new Intl.NumberFormat('en', { style: 'currency', currency }).resolvedOptions().maximumFractionDigits ?? 0

export const formatPrice = (amount: number, currency: Currency, locale: string): string => {
  const format = new Intl.NumberFormat(locale, { style: 'currency', currency })
  return format.format(amount / 10 ** priceDigits(currency))
}

export const priceText = (amount: number, currency: Currency): string => (amount === 0 ? '' : String(amount / 10 ** priceDigits(currency)))

export const priceAmount = (text: string, currency: Currency): number => Math.round(Number(text) * 10 ** priceDigits(currency))

const PRICE_MIN = 100
const PRICE_MAX = 50000

export const paidTextError = (paidText: string, price: number): string => {
  if (paidText !== '' && (price < PRICE_MIN || price > PRICE_MAX)) return 'error.priceRange'
  if (paidText === '' && price !== 0) return 'error.paidTextRequired'
  return ''
}
