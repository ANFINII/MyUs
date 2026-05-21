import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { PaymentCancelOut, PaymentCheckoutIn, PaymentCheckoutOut } from 'types/internal/payment'
import { apiPaymentCancel, apiPaymentCheckout } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postPaymentCheckout = async (request: PaymentCheckoutIn): Promise<ApiOut<PaymentCheckoutOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentCheckout, camelSnake(request)))
}

export const postPaymentCancel = async (): Promise<ApiOut<PaymentCancelOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentCancel))
}
