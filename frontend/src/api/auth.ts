import { HttpStatusCode } from 'axios'
import { apiClient, apiFormClient } from 'lib/axios'
import { LoginIn, SignupIn, User } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { camelSnake } from 'utils/functions/convertCase'
import { apiUser, apiLogin, apiLogout, apiSignup } from './uri'

export const getUser = async (): Promise<User> => {
  const data = await apiClient.get(apiUser).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const postLogin = async (request: LoginIn): Promise<MessageOut | void> => {
  const data = await apiClient.post(apiLogin, request).then((res) => {
    if (res.status === HttpStatusCode.InternalServerError) throw Error
    return res.data
  })
  return data
}

export const postLogout = async (): Promise<void> => {
  await apiClient.post(apiLogout).then((res) => {
    if (res.status === HttpStatusCode.InternalServerError) throw Error
  })
}

export const postSignup = async (request: SignupIn): Promise<MessageOut | void> => {
  const data = await apiFormClient.post(apiSignup, camelSnake(request)).then((res) => {
    if (res.status === HttpStatusCode.InternalServerError) throw Error
    return res.data
  })
  return data
}

export const postReset = async (email: string): Promise<MessageOut | void> => {
  const data = await apiFormClient.post(apiSignup, email).then((res) => {
    if (res.status === HttpStatusCode.InternalServerError) throw Error
    return res.data
  })
  return data
}
