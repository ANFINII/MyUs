import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { PaymentCheckoutIn, PaymentCheckoutOut } from 'types/internal/payment'
import { apiPaymentCheckout } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postPaymentCheckout = async (request: PaymentCheckoutIn): Promise<ApiOut<PaymentCheckoutOut>> => {
  return await apiOut(apiClient('json').post(apiPaymentCheckout, camelSnake(request)))
}
