import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient, apiFormClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { ProfileIn, ProfileOut, MypageIn, MypageOut, Follow, SearchTagOut, NotificationOut, NotificationIn } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { camelSnake } from 'utils/functions/convertCase'
import { apiProfile, apiMypage, apiFollow, apiFollower, apiSearchTag, apiNotification } from '../uri'

export const getServerProfile = async (req: Req): Promise<ProfileOut> => {
  const res = await apiServer(req, apiClient, apiProfile)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getProfile = async (): Promise<ProfileOut> => {
  const res = await apiClient.get(apiProfile)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putProfile = async (request: ProfileIn): Promise<MessageOut | void> => {
  const res = await apiFormClient.put(apiProfile, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerMypage = async (req: Req): Promise<MypageOut> => {
  const res = await apiServer(req, apiClient, apiMypage)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putMypage = async (request: MypageIn): Promise<MessageOut | void> => {
  const res = await apiFormClient.put(apiMypage, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerNotification = async (req: Req): Promise<NotificationOut> => {
  const res = await apiServer(req, apiClient, apiNotification)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getNotification = async (): Promise<NotificationOut> => {
  const res = await apiClient.get(apiNotification)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putNotification = async (request: NotificationIn): Promise<void> => {
  const res = await apiClient.put(apiNotification, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
}

export const getSearchTag = async (): Promise<SearchTagOut[]> => {
  const res = await apiClient.get(apiSearchTag)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerFollow = async (req: Req): Promise<Follow[]> => {
  const res = await apiServer(req, apiClient, apiFollow)
  if (res.status >= HttpStatusCode.BadRequest) return []
  return res.data
}

export const getServerFollower = async (req: Req): Promise<Follow[]> => {
  const res = await apiServer(req, apiClient, apiFollower)
  if (res.status >= HttpStatusCode.BadRequest) return []
  return res.data
}
