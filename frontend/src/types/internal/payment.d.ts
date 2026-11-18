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

export interface PaymentBlogCheckoutIn {
  blogUlid: string
  locale: Locale
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

export interface PaymentSellerOut {
  isAvailable: boolean
  isRegistered: boolean
  isEnabled: boolean
  currency: Currency
}

export interface PaymentSellerOnboardIn {
  locale: Locale
}

export interface PaymentSellerOnboardOut {
  url: string
}

export interface PaymentCancelOut {
  canceledAt: string
  periodEnd: string
}
