import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { PaymentCancelOut, PaymentChangeIn, PaymentCheckoutIn, PaymentCheckoutOut, PaymentMethodIn, PaymentMethodOut, PaymentPlanOut, PaymentSubscriptionOut } from 'types/internal/payment'
import { apiPaymentCancel, apiPaymentCancelRevoke, apiPaymentChange, apiPaymentCheckout, apiPaymentMethod, apiPaymentPlans, apiPaymentSubscription } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getPaymentSubscription = async (): Promise<ApiOut<PaymentSubscriptionOut>> => {
  return await apiOut(apiClient('json').get(apiPaymentSubscription))
}

export const getPaymentPlans = async (): Promise<ApiOut<PaymentPlanOut[]>> => {
  return await apiOut(apiClient('json').get(apiPaymentPlans))
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

export const postPaymentMethod = async (request: PaymentMethodIn): Promise<ApiOut<PaymentMethodOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentMethod, camelSnake(request)))
}
