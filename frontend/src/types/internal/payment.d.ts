import { Currency, Locale } from 'utils/constants/enum'

export interface Money {
  amount: number
  currency: Currency
}

export interface PaymentSubscriptionOut {
  isCanceled: boolean
  isPastDue: boolean
  periodEnd: string
}

export interface PaymentPlanOut {
  name: string
  price: Money
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

export interface PaymentMethodIn {
  locale: Locale
}

export interface PaymentMethodOut {
  url: string
}

export interface PaymentCancelOut {
  canceledAt: string
  periodEnd: string
}
