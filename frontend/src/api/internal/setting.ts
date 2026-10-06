import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ErrorOut } from 'types/internal/other'
import { ProfileOut, ProfileIn, MypageOut, MypageIn, UserNotificationOut, UserNotificationIn } from 'types/internal/user'
import { apiSettingProfile, apiSettingMypage, apiSettingNotification } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getSettingProfile = async (): Promise<ApiOut<ProfileOut>> => {
  return await apiOut(apiClient('json').get(apiSettingProfile))
}

export const putSettingProfile = async (request: ProfileIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiSettingProfile, camelSnake(request)))
}

export const getSettingMypage = async (): Promise<ApiOut<MypageOut>> => {
  return await apiOut(apiClient('json').get(apiSettingMypage))
}

export const putSettingMypage = async (request: MypageIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiSettingMypage, camelSnake(request)))
}

export const getSettingNotification = async (): Promise<ApiOut<UserNotificationOut>> => {
  return await apiOut(apiClient('json').get(apiSettingNotification))
}

export const putSettingNotification = async (request: UserNotificationIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').put(apiSettingNotification, camelSnake(request)))
}
