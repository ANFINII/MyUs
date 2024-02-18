import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { LoginRequest } from 'types/internal/auth'
import { apiAuth, apiUser, apiLogin, apiLogout } from './uri'

export const getAuth = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiAuth).then((res) => {
    return res.status === HttpStatusCode.Ok
  })
  return data
}

export const getUser = async () => {
  const data = await apiClient.get(apiUser).then((res) => {
    return res.status === HttpStatusCode.Ok
  })
  return data
}

export const postLogin = async (request: LoginRequest) => {
  const data = await apiClient.post(apiLogin, request).then((res) => {
    return res.data
  })
  return data
}

export const postLogout = async () => {
  await apiClient.post(apiLogout).then((res) => {
    if (res.status !== HttpStatusCode.NoContent) throw Error
  })
}
