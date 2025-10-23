import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { LoginIn, SignupIn } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { apiLogin, apiLogout, apiSignup } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postLogin = async (request: LoginIn): Promise<ApiOut<MessageOut | void>> => {
  return await apiOut(apiClient('json').post(apiLogin, request))
}

export const postLogout = async (): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiLogout))
}

export const postSignup = async (request: SignupIn): Promise<ApiOut<MessageOut | void>> => {
  return await apiOut(apiClient('json').post(apiSignup, camelSnake(request)))
}

export const postReset = async (email: string): Promise<ApiOut<MessageOut | void>> => {
  return await apiOut(apiClient('json').post(apiSignup, email))
}
