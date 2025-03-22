import { apiClient, apiFormClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { LoginIn, SignupIn, User } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { apiUser, apiLogin, apiLogout, apiSignup } from 'api/uri'

export const getUser = async (req?: Req): Promise<ApiOut<User>> => {
  return await apiOut(apiClient.get(apiUser, cookieHeader(req)))
}

export const postLogin = async (request: LoginIn): Promise<ApiOut<MessageOut | void>> => {
  return await apiOut(apiFormClient.post(apiLogin, request))
}

export const postLogout = async (): Promise<ApiOut<void>> => {
  return await apiOut(apiFormClient.post(apiLogout))
}

export const postSignup = async (request: SignupIn): Promise<ApiOut<MessageOut | void>> => {
  return await apiOut(apiFormClient.post(apiSignup, request))
}

export const postReset = async (email: string): Promise<ApiOut<MessageOut | void>> => {
  return await apiOut(apiFormClient.post(apiSignup, email))
}
