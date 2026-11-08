import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { PaymentCancelOut, PaymentChangeIn, PaymentCheckoutIn, PaymentCheckoutOut } from 'types/internal/payment'
import { apiPaymentCancel, apiPaymentChange, apiPaymentCheckout } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postPaymentCheckout = async (request: PaymentCheckoutIn): Promise<ApiOut<PaymentCheckoutOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentCheckout, camelSnake(request)))
}

export const postPaymentCancel = async (): Promise<ApiOut<PaymentCancelOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentCancel))
}

export const postPaymentChange = async (request: PaymentChangeIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiPaymentChange, camelSnake(request)))
}
