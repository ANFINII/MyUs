import { apiClient } from 'lib/axios/internal'
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

export const getSettingMypage = async (req?: Req): Promise<ApiOut<MypageOut>> => {
  return await apiOut(apiClient.get(apiSettingMypage, cookieHeader(req)))
}

export const putSettingMypage = async (request: MypageIn): Promise<ApiOut<MessageOut>> => {
  return await apiOut(apiClient.put(apiSettingMypage, camelSnake(request)))
}

export const getSettingNotification = async (req?: Req): Promise<ApiOut<UserNotificationOut>> => {
  return await apiOut(apiClient.get(apiSettingNotification, cookieHeader(req)))
}

export const putSettingNotification = async (request: UserNotificationIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient.put(apiSettingNotification, camelSnake(request)))
}
