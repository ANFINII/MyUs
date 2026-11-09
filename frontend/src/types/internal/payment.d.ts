import { Locale } from 'utils/constants/enum'

export interface PaymentSubscriptionOut {
  isCanceled: boolean
  periodEnd: string
}

export interface PaymentCheckoutIn {
  plan: string
  locale: Locale
}

export interface PaymentCheckoutOut {
  url: string
}

export interface PaymentChangeIn {
  plan: string
}

export interface PaymentCancelOut {
  canceledAt: string
  periodEnd: string
}
