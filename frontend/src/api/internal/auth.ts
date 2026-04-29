import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { LoginIn, PasswordChangeIn, PasswordResetIn, PasswordResetVerifyOut, SignupIn, SignupVerifyOut, WithdrawalIn } from 'types/internal/auth'
import {
  apiLogin,
  apiLogout,
  apiPasswordChange,
  apiPasswordReset,
  apiPasswordResetEmail,
  apiPasswordResetVerify,
  apiSignup,
  apiSignupEmail,
  apiSignupVerify,
  apiWithdrawal,
} from 'api/uri'
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

export const postPasswordReset = async (request: PasswordResetIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiPasswordReset, camelSnake(request)))
}

export const postPasswordResetEmail = async (email: string): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiPasswordResetEmail, { email }))
}

export const getPasswordResetVerify = async (token: string): Promise<ApiOut<PasswordResetVerifyOut>> => {
  return await apiOut(apiClient('json').get(apiPasswordResetVerify, { params: { token } }))
}

export const postPasswordChange = async (request: PasswordChangeIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiPasswordChange, camelSnake(request)))
}

export const postWithdrawal = async (request: WithdrawalIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').post(apiWithdrawal, request))
}
