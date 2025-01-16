import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { Req } from 'types/global'
import { Follow, NotificationOut, SearchTagOut } from 'types/internal/auth'
import { apiFollow, apiFollower, apiNotification, apiSearchTag } from '../uri'

export const getSearchTag = async (req?: Req): Promise<SearchTagOut[]> => {
  const res = await apiClient.get(apiSearchTag, cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getFollow = async (req?: Req, search?: string): Promise<Follow[]> => {
  const res = await apiClient.get(apiFollow, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getFollower = async (req?: Req, search?: string): Promise<Follow[]> => {
  const res = await apiClient.get(apiFollower, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getNotification = async (req?: Req): Promise<NotificationOut> => {
  const res = await apiClient.get(apiNotification, cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}
