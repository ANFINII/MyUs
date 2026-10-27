import { Locale } from 'utils/constants/enum'

export interface PaymentCheckoutIn {
  plan: string
  locale: Locale
}

export interface PaymentCheckoutOut {
  url: string
}

export interface PaymentCancelOut {
  canceledAt: string
  periodEnd: string
}
