import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { MessageOut } from 'types/internal/other'
import { ProfileOut, ProfileIn, MypageOut, MypageIn, UserNotificationOut, UserNotificationIn } from 'types/internal/user'
import { apiSettingProfile, apiSettingMypage, apiSettingNotification } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getSettingProfile = async (req?: Req): Promise<ApiOut<ProfileOut>> => {
  return await apiOut(apiClient('json').get(apiSettingProfile, cookieHeader(req)))
}

export const putSettingProfile = async (request: ProfileIn): Promise<ApiOut<MessageOut>> => {
  return await apiOut(apiClient('form').put(apiSettingProfile, camelSnake(request)))
}

export const getSettingMypage = async (req?: Req): Promise<ApiOut<MypageOut>> => {
  return await apiOut(apiClient('json').get(apiSettingMypage, cookieHeader(req)))
}

export const putSettingMypage = async (request: MypageIn): Promise<ApiOut<MessageOut>> => {
  return await apiOut(apiClient('form').put(apiSettingMypage, camelSnake(request)))
}

export const getSettingNotification = async (req?: Req): Promise<ApiOut<UserNotificationOut>> => {
  return await apiOut(apiClient('json').get(apiSettingNotification, cookieHeader(req)))
}

export const putSettingNotification = async (request: UserNotificationIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').put(apiSettingNotification, camelSnake(request)))
}
