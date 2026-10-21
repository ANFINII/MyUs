import { useTranslation } from 'react-i18next'
import { Currency } from 'utils/constants/enum'

interface OutProps {
  formatPrice: (amount: number, currency: Currency) => string
}

export function usePrice(): OutProps {
  const { i18n } = useTranslation()
  const locale = i18n.language

  const formatPrice = (amount: number, currency: Currency): string => {
    return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount)
  }

  return { formatPrice }
}
