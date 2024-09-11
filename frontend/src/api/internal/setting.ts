import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient, apiFormClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { ProfileIn, ProfileOut, MypageIn, MypageOut, UserNotificationIn, UserNotificationOut } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { camelSnake } from 'utils/functions/convertCase'
import { apiSettingProfile, apiSettingMypage, apiSettingNotification } from '../uri'

export const getServerSettingProfile = async (req: Req): Promise<ProfileOut> => {
  const res = await apiServer(req, apiClient, apiSettingProfile)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putSettingProfile = async (request: ProfileIn): Promise<MessageOut | void> => {
  const res = await apiFormClient.put(apiSettingProfile, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerSettingMypage = async (req: Req): Promise<MypageOut> => {
  const res = await apiServer(req, apiClient, apiSettingMypage)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putSettingMypage = async (request: MypageIn): Promise<MessageOut | void> => {
  const res = await apiFormClient.put(apiSettingMypage, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerSettingNotification = async (req: Req): Promise<UserNotificationOut> => {
  const res = await apiServer(req, apiClient, apiSettingNotification)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getSettingNotification = async (): Promise<UserNotificationOut> => {
  const res = await apiClient.get(apiSettingNotification)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putSettingNotification = async (request: UserNotificationIn): Promise<void> => {
  const res = await apiClient.put(apiSettingNotification, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
}
