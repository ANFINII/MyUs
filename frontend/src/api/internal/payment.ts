import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { PaymentCancelOut, PaymentChangeIn, PaymentCheckoutIn, PaymentCheckoutOut, PaymentSubscriptionOut } from 'types/internal/payment'
import { apiPaymentCancel, apiPaymentCancelRevoke, apiPaymentChange, apiPaymentCheckout, apiPaymentSubscription } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getPaymentSubscription = async (): Promise<ApiOut<PaymentSubscriptionOut>> => {
  return await apiOut(apiClient('json').get(apiPaymentSubscription))
}

export const postPaymentCheckout = async (request: PaymentCheckoutIn): Promise<ApiOut<PaymentCheckoutOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentCheckout, camelSnake(request)))
}

export const postPaymentCancel = async (): Promise<ApiOut<PaymentCancelOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentCancel))
}

export const postPaymentCancelRevoke = async (): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiPaymentCancelRevoke))
}

export const postPaymentChange = async (request: PaymentChangeIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiPaymentChange, camelSnake(request)))
}
