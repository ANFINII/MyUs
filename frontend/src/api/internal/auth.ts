import { HttpStatusCode } from 'axios'
import { apiClient, apiFormClient } from 'lib/axios'
import { LoginIn, SignupIn, User } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { camelSnake } from 'utils/functions/convertCase'
import { apiUser, apiLogin, apiLogout, apiSignup } from '../uri'

export const getUser = async (): Promise<User> => {
  const res = await apiClient.get(apiUser)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postLogin = async (request: LoginIn): Promise<MessageOut | void> => {
  const res = await apiClient.post(apiLogin, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postLogout = async (): Promise<void> => {
  const res = await apiClient.post(apiLogout)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
}

export const postSignup = async (request: SignupIn): Promise<MessageOut | void> => {
  const res = await apiFormClient.post(apiSignup, camelSnake(request))
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postReset = async (email: string): Promise<MessageOut | void> => {
  const res = await apiFormClient.post(apiSignup, email)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}
