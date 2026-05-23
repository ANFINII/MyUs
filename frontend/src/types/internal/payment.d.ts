export interface PaymentCheckoutIn {
  plan: string
}

export interface PaymentCheckoutOut {
  url: string
}

export interface PaymentCancelOut {
  canceledAt: string
  periodEnd: string
}
