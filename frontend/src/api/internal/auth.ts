import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { LoginIn, SignupIn, SignupVerifyOut } from 'types/internal/auth'
import { apiLogin, apiLogout, apiSignup, apiSignupEmail, apiSignupVerify } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postLogin = async (request: LoginIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiLogin, request))
}

export const postLogout = async (): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiLogout))
}

export const postSignup = async (request: SignupIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiSignup, camelSnake(request)))
}

export const postSignupEmail = async (email: string): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiSignupEmail, { email }))
}

export const getSignupVerify = async (token: string): Promise<ApiOut<SignupVerifyOut>> => {
  return await apiOut(apiClient('json').get<SignupVerifyOut>(apiSignupVerify, { params: { token } }))
}

export const postReset = async (email: string): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiSignup, email))
}
