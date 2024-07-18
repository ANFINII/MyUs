import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { LoginIn, User } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { apiAuth, apiUser, apiLogin, apiLogout } from './uri'

export const getServerAuth = async (req: Req): Promise<boolean> => {
  const data = await apiServer(req, apiClient, apiAuth).then((res) => {
    return res.status === HttpStatusCode.Ok
  })
  return data
}

export const getUser = async (): Promise<User> => {
  const data = await apiClient.get(apiUser).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const postLogin = async (request: LoginIn): Promise<MessageOut | void> => {
  const data = await apiClient.post(apiLogin, request).then((res) => {
    return res.data
  })
  return data
}

export const postLogout = async (): Promise<void> => {
  await apiClient.post(apiLogout)
}
