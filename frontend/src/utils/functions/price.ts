import { Currency } from 'utils/constants/enum'

export const formatPrice = (amount: number, currency: Currency, locale: string): string => {
  return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount)
}
