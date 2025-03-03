import { HttpStatusCode } from 'axios'
import { apiClient, apiFormClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { Req } from 'types/global'
import { LoginIn, SignupIn, User } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { apiUser, apiLogin, apiLogout, apiSignup } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getUser = async (req?: Req): Promise<User> => {
  const res = await apiClient.get(apiUser, cookieHeader(req))
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
