import { HttpStatusCode } from 'axios'
import { apiClient, apiFormClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { ProfileIn, ProfileOut, MypageIn, MypageOut, UserNotificationIn, UserNotificationOut } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { apiSettingProfile, apiSettingMypage, apiSettingNotification } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getSettingProfile = async (req?: Req): Promise<ApiOut<ProfileOut>> => {
  return await apiOut(apiClient.get(apiSettingProfile, cookieHeader(req)))
}

export const putSettingProfile = async (request: ProfileIn): Promise<ApiOut<MessageOut>> => {
  return await apiOut(apiClient.put(apiSettingProfile, camelSnake(request)))
}

export const getSettingMypage = async (req?: Req): Promise<MypageOut> => {
  const res = await apiClient.get(apiSettingMypage, cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putSettingMypage = async (request: MypageIn): Promise<MessageOut | void> => {
  const res = await apiFormClient.put(apiSettingMypage, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getSettingNotification = async (req?: Req): Promise<UserNotificationOut> => {
  const res = await apiClient.get(apiSettingNotification, cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const putSettingNotification = async (request: UserNotificationIn): Promise<void> => {
  const res = await apiClient.put(apiSettingNotification, camelSnake(request))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
}
