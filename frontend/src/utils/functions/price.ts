import { Currency } from 'utils/constants/enum'

export const formatPrice = (amount: number, currency: Currency, locale: string): string => {
  const format = new Intl.NumberFormat(locale, { style: 'currency', currency })
  const digits = format.resolvedOptions().maximumFractionDigits ?? 0
  return format.format(amount / 10 ** digits)
}
